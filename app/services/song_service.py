from app.api.models.musci import Song
from app.extensions import db
from flask import current_app as app
from ..utils.helper import filter_data


class SongService:
    @staticmethod
    def get_all_songs():
        try:
            return Song.query.all()
        except Exception as e:
            app.logger.error("Error retrieving all songs: %s", e)
            return []

    @staticmethod
    def get_song_by_id(song_id):
        try:

            return Song.query.get(song_id)
        except Exception as e:
            app.logger.error("Error retrieving song with id %s: %s", song_id, e)
            return None

    @staticmethod
    def create_song(data):
        # 检查必要字段

        if 'title' not in data or 'singer_id' not in data:
            app.logger.warning("Missing 'title' or 'singer_id' in data for song creation.")
            return None
        try:
            filtered_data = filter_data(Song, data)
            song = Song(**filtered_data)

            db.session.add(song)
            db.session.commit()
            return song
        except Exception as e:
            db.session.rollback()
            app.logger.error("Error creating song: %s", e)
            return None

    @staticmethod
    def update_song(song_id, data):
        song = SongService.get_song_by_id(song_id)
        if not song:
            app.logger.warning("Song with id %s not found for update.", song_id)
            return None
        try:
            song.title = data.get('title', song.title)

            filtered_data = filter_data(data, Song)
            # 动态更新 Singer 实例的属性
            for key, value in filtered_data.items():
                setattr(song, key, value)
            db.session.commit()
            return song
        except Exception as e:
            db.session.rollback()
            app.logger.error("Error updating song with id %s: %s", song_id, e)
            return None

    @staticmethod
    def delete_song(song_id):
        song = SongService.get_song_by_id(song_id)
        if not song:
            app.logger.warning("Song with id %s not found for deletion.", song_id)
            return False
        try:
            db.session.delete(song)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            app.logger.error("Error deleting song with id %s: %s", song_id, e)
            return False
