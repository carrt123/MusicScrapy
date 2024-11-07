from app.config import MusicSetting

setting = MusicSetting()


def singer_url():
    for i in range(0, 3):
        url = setting.start_url.format(index=80 * i, cur_page=i, area=2, sex=-100)
        print(url)


def song_url():
    url = setting.song_list_url.format(singer_mid="0017DdFg2hCIao", begin=0, num=100)
    print(url)


song_url()
