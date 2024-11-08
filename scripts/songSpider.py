import random
import time
import requests
import sqlite3
import logging
from fake_useragent import UserAgent
from app.config import MusicSetting
from scripts import SongSetting


# 配置日志
def configure_logging(log_file='../logs/song_spider.log'):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Logging configured successfully")


class DatabaseManager:
    """负责数据库操作的类"""

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def insert_song_singer(self, singer_id, song_id):
        sql = "INSERT INTO song_singer (singer_id, song_id) VALUES (?, ?)"
        try:
            self.cursor.execute(sql, (singer_id, song_id))
            self.conn.commit()
            logging.info(f"Inserted song_singer: {singer_id}, {song_id}")
            print(f"Inserted song_singer: {singer_id}, {song_id}")
        except sqlite3.IntegrityError as e:
            logging.error(f"Error inserting song_singer: {e}")
            self.conn.rollback()

    def insert_song(self, song_data):
        sql = """
            INSERT INTO song (id, title, subtitle, type, language, time_public, mid, album, song_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            self.cursor.execute(sql, (
                song_data['id'],
                song_data['title'],
                song_data['subtitle'],
                song_data['type'],
                song_data['language'],
                song_data['time_public'],
                song_data['mid'],
                song_data['album'],
                song_data['song_url']
            ))
            self.conn.commit()
            logging.info(f"Inserted song {song_data['title']} successfully")
            print(f"Inserted song {song_data['title']} successfully")
        except sqlite3.Error as e:
            self.conn.rollback()
            logging.error(f"Failed to insert song {song_data['title']}: {e}")

    def get_singer_mids(self, limit=1):
        """获取指定数量的歌手mid"""
        self.cursor.execute("SELECT mid FROM singer LIMIT ?", (limit,))
        return [row[0] for row in self.cursor.fetchall()]

    def close(self):
        self.conn.close()
        logging.info("Database connection closed")


class RequestHandler:
    """负责处理API请求和重试机制的类"""

    def __init__(self, user_agent, retry_delay, max_retries):
        self.user_agent = user_agent
        self.retry_delay = retry_delay
        self.max_retries = max_retries

    def fetch_data(self, url, mid):
        headers = {"User-Agent": self.user_agent.random}
        delay = self.retry_delay

        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                logging.info(f"Successfully fetched data for singer_mid {mid}")
                return response.json()['singerSongList']['data']['songList']
            except requests.RequestException as e:
                logging.error(f"Request error on attempt {attempt + 1} for URL {url}: {e}")
                time.sleep(delay)
                delay *= 2

        logging.error(f"Failed to fetch data for singer_mid {mid} after {self.max_retries} attempts")
        return None


class SongSpider:
    """主爬虫逻辑类，处理页面循环和数据插入"""

    def __init__(self, db_manager, request_handler, url_setting, spider_setting):
        self.db_manager = db_manager
        self.request_handler = request_handler
        self.url_setting = url_setting
        self.spider_setting = spider_setting
        self.genre_dict = spider_setting.genre_dict
        self.language_dict = spider_setting.language_dict

    def process_song(self, song_info):
        """处理并插入单个歌曲的信息和歌手信息"""
        song_data = {
            'id': song_info['id'],
            'title': song_info['title'],
            'subtitle': song_info['subtitle'],
            'type': song_info['type'],
            'language': song_info['language'],
            'time_public': song_info['time_public'] if song_info['time_public'] else None,
            'mid': song_info['mid'],
            'album': song_info['album']['name'],
            'song_url': self.url_setting.song_url.format(song_mid=song_info['mid'])
        }

        self.db_manager.insert_song(song_data)

        singer_ids = [singer['id'] for singer in song_info['singer']]
        for singer_id in singer_ids:
            self.db_manager.insert_song_singer(singer_id, song_data['id'])

    def run(self, begin, num):
        """执行爬虫，遍历获取歌手的歌曲列表"""
        logging.info(f"Starting songSpider with begin={begin}, num={num}")
        headers = {'User-Agent': UserAgent().random}
        singer_mids = self.db_manager.get_singer_mids()
        for mid in singer_mids:
            url = self.url_setting.song_list_url.format(singer_mid=mid, begin=begin, num=num)
            song_list = self.request_handler.fetch_data(url, mid)
            if not song_list:
                logging.error(f"No data returned for singer_mid {mid}, skipping.")
                continue

            for song in song_list:
                self.process_song(song['songInfo'])

            time.sleep(random.uniform(3, 5))


def main():
    # 配置日志
    configure_logging()

    # 初始化设置
    url_setting = MusicSetting()
    spider_setting = SongSetting()
    user_agent = UserAgent()

    # 创建组件实例
    db_manager = DatabaseManager("../instance/development.db")
    request_handler = RequestHandler(user_agent, retry_delay=spider_setting.retry_delay,
                                     max_retries=spider_setting.max_retries)
    song_spider = SongSpider(db_manager, request_handler, url_setting, spider_setting)

    # 执行爬虫任务
    try:
        song_spider.run(begin=0, num=50)
    finally:
        db_manager.close()


if __name__ == "__main__":
    main()
