- **singer_name**: 歌手名称，数组形式，因为一首歌可能由多名歌手合唱
- **song_name**: 歌曲名称
- **subtitle**: 歌曲的子标题
- **album_name**: 专辑名称
- **singer_id**: 歌手 id，数组形式
- **singer_mid**: 歌手的 mid，数组形式
- **song_time_public**: 歌曲发行时间
- **song_type**: 歌曲类型
- **language**: 歌曲语种
- **song_id**: 歌曲 id
- **song_mid**: 歌曲 mid
- **song_url**: 歌曲播放的 URL
- **lyric**: 歌词
- **hot_comments**: 歌曲的精彩评论（此处只爬取了歌曲的精彩评论，部分比较冷门的歌曲有最新评论，但是没有精彩评论），数组形式。若无精彩评论，置为 `"null"`
  - **comment_name**: 评论者的昵称
  - **comment_text**: 评论内容






- **area**: 歌手的地域(内地、港台、欧美等)。-100:全部、200:内地、2:港台、5:欧美、4:日本、3:韩国、6:其他
- **genre**: 歌手风格(流行、嘻哈等)。-100：全部、1：流行、6：嘻哈、2：摇滚、4：电子、3：民谣、8：R&B、10：民歌、9：轻音乐、5：爵士、14：古典、25：乡村、20：蓝调
- **cur_page**: 当前歌手列表的页码
- **index**:cur_page*page_size(index表示当前页的起始index，page_size表示每一页歌手的数量)

