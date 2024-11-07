import urllib.parse
# 原始编码的 URL 参数
singer_url = "%7B%22singerList%22%3A%7B%22module%22%3A%22Music.SingerListServer%22%2C%22method%22%3A%22get_singer_list%22%2C%22param%22%3A%7B%22area%22%3A2%2C%22sex%22%3A0%2C%22genre%22%3A-100%2C%22index%22%3A-100%2C%22sin%22%3A160%2C%22cur_page%22%3A2%7D%7D%7D"

song_url = "%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%2C%22singerSongList%22%3A%7B%22method%22%3A%22GetSingerSongList%22%2C%22param%22%3A%7B%22order%22%3A1%2C%22singerMid%22%3A%22003LCFXH0eodXv%22%2C%22begin%22%3A0%2C%22num%22%3A100%7D%2C%22module%22%3A%22musichall.song_list_server%22%7D%7D"
# 解码
decoded_data = urllib.parse.unquote(song_url)

# 输出结果
print(decoded_data)
