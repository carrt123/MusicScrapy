# - *- coding: utf-8 -*-

from marshmallow import Schema, fields, post_load, validate
from app.api.models.musci import Singer


class SingerSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=20), describe="歌手名字")
    sex = fields.String(validate=validate.OneOf(['男', '女']), describe="歌手性别")
    country = fields.String(validate=validate.Length(min=1, max=20), describe="歌手国籍")
    picture = fields.String(validate=validate.Length(min=1, max=100), describe="歌手图片")
    mid = fields.String(validate=validate.Length(min=1, max=20), describe="歌曲mid")

    @post_load
    def make_singer(self, data, **kwargs):
        # 在反序列化时，自动生成 Singer 对象
        if 'id' in data:
            return Singer(**data)
        return data



