from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.singer_service import SingerService

singer_ns = Namespace('singers', description='歌手API资源')

singer_post_model = singer_ns.model('SingerPost', {
    'id': fields.Integer(required=True, description='歌手唯一标识符'),
    'name': fields.String(required=True, description='歌手名字'),
    'country': fields.String(description='歌手来自地区'),
    'sex': fields.String(description='歌手性别'),
    'picture': fields.String(description='歌手照片'),
    'mid': fields.String(description='歌手mid')
})

singer_put_model = singer_ns.model('SingerPut', {
    'country': fields.String(description='歌手来自地区'),
    'sex': fields.String(description='歌手性别'),
    'picture': fields.String(description='歌手照片'),
    'mid': fields.String(description='歌手mid')
})


class SingerResource(Resource):
    @singer_ns.param('page', description='当前处于那一页')
    @singer_ns.param('per_page', description='每页显示多少条数据')
    @singer_ns.param('name', description='歌手名字')
    def get(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        name = request.args.get('name', default=None, type=str)
        return SingerService.get_all_singers(page, per_page, name)

    @singer_ns.expect(singer_post_model)
    def post(self):
        data = request.get_json()
        return SingerService.create_singer(data)


class SingerDetailResource(Resource):
    def get(self, singer_id):
        return SingerService.get_singer_by_id(singer_id)

    @singer_ns.expect(singer_put_model)
    def put(self, singer_id):
        data = request.get_json()
        return SingerService.update_singer(singer_id, data)

    def delete(self, singer_id):
        return SingerService().delete_singer(singer_id)


singer_ns.add_resource(SingerResource, '/')
singer_ns.add_resource(SingerDetailResource, '/<int:singer_id>')
