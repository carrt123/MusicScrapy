from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.song_service import SongService
from app.utils.validators import validate_song_data

song_ns = Namespace('songs', description='歌曲API资源')

song_post_model = song_ns.model('SongPost', {
    'id': fields.Integer(required=True, description='歌曲ID'),
    'title': fields.String(required=True, description='歌曲标题'),
    "type": fields.Integer(required=True, description='歌曲类型'),
    "language": fields.Integer(required=True, description='歌曲语言'),
    "mid": fields.String(required=True, description='歌曲mid'),
    "subtitle": fields.String(description='歌曲副标题'),
    "album": fields.String(description='歌曲专辑名字'),
    "time_public": fields.DateTime(description='歌曲发布时间')
})

song_put_model = song_ns.model('SongPut', {
    "type": fields.Integer(description='歌曲类型'),
    "language": fields.Integer(description='歌曲语言'),
    "subtitle": fields.String(description='歌曲副标题'),
    "album": fields.String(description='歌曲专辑名字'),
    "time_public": fields.DateTime(description='歌曲发布时间')
})


class SongResource(Resource):
    @song_ns.param('page', description='当前处于那一页')
    @song_ns.param('per_page', description='每页显示多少条数据')
    @song_ns.param('title', description='歌曲标题')
    def get(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        title = request.args.get('title', default=None, type=str)
        return SongService().get_all_songs(page, per_page, title)

    @song_ns.expect(song_post_model)
    def post(self):
        data = request.get_json()
        return SongService().create_song(data)


class SongDetailResource(Resource):
    def get(self, song_id):
        return SongService().get_song_by_id(song_id)

    @song_ns.expect(song_put_model)
    def put(self, song_id):
        data = request.get_json()
        return SongService().update_song(song_id, data)

    def delete(self, song_id):
        return SongService.delete_song(song_id)


song_ns.add_resource(SongResource, '/')
song_ns.add_resource(SongDetailResource, '/<int:song_id>')
