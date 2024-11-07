import os
from dotenv import load_dotenv

load_dotenv()


class MusicSetting:
    start_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?data=%7B%22singerList%22%3A%7B%22module%22%3A%22Music.SingerListServer' \
                '%22%2C%22method%22%3A%22get_singer_list%22%2C%22param%22%3A%7B%22area%22%3A{area}%2C%22sex%22%3A{sex}%2C%22genr' \
                'e%22%3A-100%2C%22index%22%3A-100%2C%22sin%22%3A{index}%2C%22cur_page%22%3A{cur_page}%7D%7D%7D'

    song_list_url = "https://u.y.qq.com/cgi-bin/musicu.fcg?data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%2C%22singerSongList%22%3A%7B%22method%22%3A%22GetSingerSongList%22%2C%22param%22%3A%7B%22order%22%3A1%2C%22singerMid%22%3A%22{singer_mid}%22%2C%22begin%22%3A{begin}%2C%22num%22%3A{num}%7D%2C%22module%22%3A%22musichall.song_list_server%22%7D%7D"
    # 获取歌词，需要指定song_id
    lyric_url = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_yqq.fcg?nobase64=1&musicid={song_id}&format=json"
    # 获取歌词时，必须带上该referer header,需要指定song_mid
    referer = "https://y.qq.com/n/yqq/song/{song_mid}.html"
    # 歌曲评论，需要song_id
    comment_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?biztype=1&topid={song_id}&cmd=8&pagenum={pagenum}&pagesize={pagesize}'
    # 歌曲的url，需要指定song_mid
    song_url = "https://y.qq.com/n/yqq/song/{song_mid}.html"


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    LOG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../logs/app.log')


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///production.db"


# 配置字典，便于通过环境变量选择
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}


def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return config.get(env, DevelopmentConfig)



