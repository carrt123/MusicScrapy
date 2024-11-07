import random
import time
import requests
import sqlite3
import logging
from fake_useragent import UserAgent
from app.config import MusicSetting
from scripts import SingerSetting


# 日志配置
def configure_logging(log_file='../logs/singer_spider.log'):
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

    def insert_singer(self, singer):
        sql = "INSERT INTO singer (id, name, picture, country, mid, sex) VALUES (?, ?, ?, ?, ?, ?);"
        try:
            self.cursor.execute(sql, (
                singer['id'], singer['name'], singer['picture'],
                singer['country'], singer['mid'], singer['sex']
            ))
            self.conn.commit()
            logging.info(f"Inserted singer {singer['name']} (ID: {singer['id']}) into database")
        except sqlite3.Error as e:
            logging.error(f"Database error for singer {singer['name']} (ID: {singer['id']}): {e}")
            self.conn.rollback()

    def close(self):
        self.conn.close()
        logging.info("Database connection closed")


class RequestHandler:
    """负责处理API请求和重试机制的类"""

    def __init__(self, user_agent, retry_delay, max_retries):
        self.user_agent = user_agent
        self.retry_delay = retry_delay
        self.max_retries = max_retries

    def fetch_data(self, url):
        headers = {"User-Agent": self.user_agent.random}
        delay = self.retry_delay

        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                logging.info(f"Successfully fetched data from URL: {url}")
                return response.json().get('singerList', {}).get('data', {})
            except requests.RequestException as e:
                logging.error(f"Request error on attempt {attempt + 1} for URL {url}: {e}")
                time.sleep(delay)
                delay *= 2

        logging.error(f"Failed to fetch data from URL: {url} after {self.max_retries} attempts")
        return None


class SingerSpider:
    """主爬虫逻辑类，处理页面循环和数据插入"""

    def __init__(self, db_manager, request_handler, url_setting, spider_setting):
        self.db_manager = db_manager
        self.request_handler = request_handler
        self.url_setting = url_setting
        self.spider_setting = spider_setting
        self.country_dict = spider_setting.country_dict
        self.sex_dict = spider_setting.sex_dict

    def run(self, pages, area_ty, sex_ty):
        logging.info(f"Starting singerSpider with pages={pages}, area_ty={area_ty}, sex_ty={sex_ty}")

        for i in random.sample(range(1, pages + 1), pages):
            url = self.url_setting.start_url.format(index=80 * (i - 1), cur_page=i, area=area_ty, sex=sex_ty)
            data = self.request_handler.fetch_data(url)

            if not data:
                logging.error(f"No data returned for page {i}, skipping.")
                continue

            for singer in data.get('singerlist', []):
                singer_data = {
                    'id': singer['singer_id'],
                    'name': singer['singer_name'],
                    'picture': singer['singer_pic'],
                    'country': self.country_dict.get(area_ty, "Unknown"),
                    'mid': singer['singer_mid'],
                    'sex': self.sex_dict.get(sex_ty, "Unknown"),
                }
                self.db_manager.insert_singer(singer_data)

            logging.info(f"Finished processing page: {i} sex: {sex_ty} area: {area_ty}")
            print(f"Finished processing page: {i} sex: {sex_ty} area: {area_ty}")

            # 随机延时避免被反爬
            time.sleep(random.uniform(3, 5))


def main():
    # 配置日志
    configure_logging()

    # 初始化设置和代理头
    url_setting = MusicSetting()
    spider_setting = SingerSetting()
    user_agent = UserAgent()

    # 创建组件实例
    db_manager = DatabaseManager("../instance/development.db")
    request_handler = RequestHandler(user_agent, retry_delay=spider_setting.retry_delay,
                                     max_retries=spider_setting.max_retries)
    singer_spider = SingerSpider(db_manager, request_handler, url_setting, spider_setting)

    # 执行爬虫任务
    try:
        singer_spider.run(pages=5, area_ty="200", sex_ty="0")
        singer_spider.run(pages=5, area_ty="200", sex_ty="1")
    finally:
        db_manager.close()


if __name__ == "__main__":
    main()
