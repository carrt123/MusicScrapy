from marshmallow import Schema, fields, post_load, validate
from app.api.models.musci import Song


class SongSchema(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=50), describe="歌曲名称")
    type = fields.Integer(required=True, validate=validate.Range(0), describe="歌曲类型")
    language = fields.Integer(required=True, validate=validate.Range(0), describe="歌曲语言")
    time_public = fields.DateTime(allow_none=True, describe="歌曲发布时间")
    mid = fields.String(required=True, describe="单首歌曲mid")
    subtitle = fields.String(allow_none=True,describe="歌曲副标题")
    album = fields.String(allow_none=True,validate=validate.Length(min=1, max=50), describe="歌曲所属专辑名称")

    @post_load
    def make_song(self, data, **kwargs):
        if 'id' in data:
            return Song(**data)
        return data
