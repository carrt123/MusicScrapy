from app.api.models.musci import Song
from app.extensions import db
from flask import current_app as app
from marshmallow import ValidationError
from ..schemas.song_schema import SongSchema


class SongService:
    @staticmethod
    def get_all_songs(page: int, per_page: int, title: str = None):
        try:
            app.logger.info("View songs with pagination")
            query = Song.query
            if title:
                query = query.filter(Song.title.like(f"%{title}%"))
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            schema = SongSchema(many=True)
            return {
                "success": True,
                "code": 200,
                "msg": "Success",
                "data": {
                    "songs": schema.dump(pagination.items),
                    "total": pagination.total,
                }
            }
        except Exception as e:
            app.logger.error("Error retrieving paginated songs: %s", e)
            return {
                "success": False,
                "code": 500,
                "msg": "An error occurred while retrieving songs."
            }

    @staticmethod
    def get_song_by_id(song_id: int):
        schema = SongSchema()
        try:
            app.logger.info("View song with id %s", song_id)
            song = Song.query.get(song_id)
            if song:
                return {
                    "success": True,
                    "code": 200,
                    "msg": "Success",
                    "data": schema.dump(song)
                }
            return {
                "success": False,
                "code": 404,
                "msg": f"Song with id {song_id} not found."
            }
        except Exception as e:
            app.logger.error("Error retrieving song with id %s: %s", song_id, e)
            return {
                "success": False,
                "code": 500,
                "msg": "An error occurred while retrieving song."
            }

    @staticmethod
    def create_song(data: dict):
        if Song.query.get(data.get('id')):
            app.logger.info("Song with id %s already exists." % data.get('id'))
            return {
                "success": False,
                "code": 400,
                "msg": f"Song with id {data['id']} already exists."
            }
        schema = SongSchema()
        try:
            song = schema.load(data)
        except ValidationError as e:
            app.logger.error("Validation error during song creation: %s", e.messages)
            return {
                "success": False,
                "code": 400,
                "msg": "Invalid data provided for song creation."
            }
        try:
            db.session.add(song)
            db.session.commit()
            app.logger.info("Song with id %s created successfully.", song.id)
            return {
                "success": True,
                "code": 201,
                "msg": "Song created successfully",
                "data": schema.dump(song)
            }
        except Exception as e:
            db.session.rollback()
            app.logger.error("Error creating song: %s", e)
            return {
                "success": False,
                "code": 500,
                "msg": "Error creating song."
            }

    @staticmethod
    def update_song(song_id: int, data: dict):
        song = Song.query.get(song_id)
        if not song:
            app.logger.warning("Song with id %s not found for update.", song_id)
            return {
                "success": False,
                "code": 404,
                "msg": f"Song with id {song_id} not found."
            }
        schema = SongSchema()
        try:
            updated_data = schema.load(data, partial=True)
            for key, value in updated_data.items():
                setattr(song, key, value)
            db.session.commit()
            app.logger.info("Song with id %s updated successfully", song_id)
            return {
                "success": True,
                "code": 200,
                "msg": "Song updated successfully",
                "data": schema.dump(song)
            }
        except ValidationError as e:
            app.logger.error("Validation error during song update: %s", e.messages)
            return {
                "success": False,
                "code": 400,
                "msg": "Invalid data provided for song update."
            }
        except Exception as e:
            db.session.rollback()
            app.logger.error("Error updating song with id %s: %s", song_id, e)
            return {
                "success": False,
                "code": 500,
                "msg": f"Error updating song with id {song_id}."
            }

    @staticmethod
    def delete_song(song_id: int):
        song = Song.query.get(song_id)
        if not song:
            app.logger.warning("Song with id %s not found for deletion.", song_id)
            return {
                "success": False,
                "code": 404,
                "msg": f"Song with id {song_id} not found."
            }
        try:
            db.session.delete(song)
            db.session.commit()
            app.logger.info("Song with id %s deleted successfully", song_id)
            return {
                "success": True,
                "code": 200,
                "msg": "Song deleted successfully."
            }
        except Exception as e:
            db.session.rollback()
            app.logger.error("Error deleting song with id %s: %s", song_id, e)
            return {
                "success": False,
                "code": 500,
                "msg": f"Error deleting song with id {song_id}."
            }
