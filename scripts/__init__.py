# -*- coding: utf-8 -*-

class SingerSetting:
    country_dict = {
        "2": "港台",
        "5": "欧美",
        "4": "日本",
        "3": "韩国",
        "200": "内地",
        "6": "其他"
    }

    sex_dict = {
        "0": "男",
        "1": "女"
    }

    max_retries = 3
    retry_delay = 1


class SongSetting:
    genre_dict = {
        "1": "流行",
        "2": "摇滚",
        "3": "民谣",
        "4": "电子",
        "6": "嘻哈",
        "10": "民歌",
        "20": "蓝调",
        "9": "轻音乐",
        "5": "爵士",
        "25": "乡村",
        "8": "R&B",
        "19": "国风",
        "33": "古典",
        "0":"Pop"
    }

    language_dict = {
        "0": "CN",
        "1": "EN"
    }

    max_retries = 3
    retry_delay = 1


s = SongSetting()
print(s.genre_dict.get("1", "未知"))