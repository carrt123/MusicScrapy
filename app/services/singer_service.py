from marshmallow import ValidationError
from app.api.models.musci import Singer
from app.extensions import db
from flask import current_app as app
from ..schemas.singer_schema import SingerSchema


class SingerService:

    @staticmethod
    def get_all_singers(page: int, per_page: int, name: str):
        try:
            app.logger.info("View singers with pagination")
            query = Singer.query
            if name:
                query = query.filter(Singer.name.like(f"%{name}%"))
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            schema = SingerSchema(many=True)
            return {
                "success": True,
                "code": 200,
                "msg": "Success",
                "data": {
                    "singers": schema.dump(pagination.items),
                    "total": pagination.total,
                }
            }
        except Exception as e:
            app.logger.error("Error retrieving paginated singers: %s", e)
            return {
                "success": False,
                "code": 500,
                "msg": "An error occurred while retrieving singers."
            }

    @staticmethod
    def get_singer_by_id(singer_id: int):
        schema = SingerSchema()
        try:
            app.logger.info("View singer with id %s", singer_id)
            singer = Singer.query.get(singer_id)
            if singer:
                return {
                    "success": True,
                    "code": 200,
                    "msg": "Success",
                    "data": schema.dump(singer)
                }
            return {
                "success": False,
                "code": 404,
                "msg": f"Singer with id {singer_id} not found."
            }
        except Exception as e:
            app.logger.error("Error retrieving singer with id %s: %s", singer_id, e)
            return {
                "success": False,
                "code": 500,
                "msg": "An error occurred while retrieving singer."
            }

    @staticmethod
    def create_singer(data: dict):
        if Singer.query.get(data.get('id')):
            app.logger.info("Singer with id %s already exists." % data.get('id'))
            return {
                "success": False,
                "code": 400,
                "msg": f"Singer with id {data['id']} already exists."
            }
        schema = SingerSchema()
        try:
            singer = schema.load(data)
        except ValidationError as e:
            app.logger.error("Validation error during singer creation: %s", e.messages)
            return {
                "success": False,
                "code": 400,
                "msg": "Invalid data."
            }
        try:
            db.session.add(singer)
            db.session.commit()
            app.logger.info("Singer with id %s created successfully.", singer.id)
            return {
                "success": True,
                "code": 201,
                "msg": "Singer created successfully",
                "data": schema.dump(singer)
            }
        except Exception as e:
            db.session.rollback()
            app.logger.error("Error creating singer: %s", e)
            return {
                "success": False,
                "code": 500,
                "msg": "Error creating singer"
            }

    @staticmethod
    def update_singer(singer_id: int, data: dict):
        singer = Singer.query.get(singer_id)
        if not singer:
            app.logger.info("Singer with id %s not found", singer_id)
            return {
                "success": False,
                "code": 404,
                "msg": f"Singer with id {singer_id} not found."
            }
        schema = SingerSchema()
        try:
            updated_data = schema.load(data, partial=True)
            for key, value in updated_data.items():
                if hasattr(singer, key):
                    setattr(singer, key, value)
        except ValidationError as e:
            app.logger.error("Validation error during singer update: %s", e.messages)
            return {
                "success": False,
                "code": 400,
                "msg": "Invalid data provided for singer update."
            }
        try:
            db.session.commit()
            app.logger.info("Singer with id %s updated successfully", singer_id)
            return {
                "success": True,
                "code": 200,
                "msg": "Singer updated successfully",
                "data": schema.dump(singer)
            }
        except Exception as e:
            db.session.rollback()
            app.logger.error("Error updating singer with id %s: %s", singer_id, e)
            return {
                "success": False,
                "code": 500,
                "msg": f"Error updating singer with id {singer_id}"
            }

    @staticmethod
    def delete_singer(singer_id: int):
        singer = Singer.query.get(singer_id)
        if not singer:
            app.logger.info("Singer with id %s not found", singer_id)
            return {
                "success": False,
                "code": 404,
                "msg": f"Singer with id {singer_id} not found."
            }
        try:
            db.session.delete(singer)
            db.session.commit()
            app.logger.info("Singer with id %s deleted successfully", singer_id)
            return {
                "success": True,
                "code": 200,
                "msg": "Singer deleted successfully"
            }
        except Exception as e:
            db.session.rollback()
            app.logger.error("Error deleting singer with id %s: %s", singer_id, e)
            return {
                "success": False,
                "code": 500,
                "msg": f"Error deleting singer with id {singer_id}"
            }
