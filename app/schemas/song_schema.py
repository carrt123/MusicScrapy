from marshmallow import Schema, fields


class SongSchema(Schema):
    song_id = fields.Integer()
    title = fields.String(required=True)
    author = fields.String(required=True)
    picture = fields.String()
