from app.extensions import db


class SongSinger(db.Model):
    __tablename__ = 'song_singer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    singer_id = db.Column(db.Integer, db.ForeignKey('singer.id'), nullable=False)

    # 定义关系， 指向歌手和歌曲
    song = db.relationship('Song', back_populates='song_singers')
    singer = db.relationship('Singer', back_populates='singer_songs')


class Singer(db.Model):
    __tablename__ = 'singer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    sex = db.Column(db.String(2))
    country = db.Column(db.String(20))
    picture = db.Column(db.String(100))
    mid = db.Column(db.String(20))

    # 关系：一个歌手可以参与多个 SongSinger 记录
    singer_songs = db.relationship('SongSinger', back_populates='singer')
    songs = db.relationship('Song', secondary='song_singer', back_populates='singers', viewonly=True)


class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=True)
    language = db.Column(db.String(10), nullable=True)
    time_public = db.Column(db.DateTime, default=None)
    mid = db.Column(db.String(20), nullable=True)
    subtitle = db.Column(db.String(50))
    album = db.Column(db.String(50))

    # 关系：一首歌可以有多个 SongSinger 记录
    song_singers = db.relationship('SongSinger', back_populates='song')
    singers = db.relationship('Singer', secondary='song_singer', back_populates='songs', viewonly=True)
