from flask_restx import Namespace, Resource, fields

from app.services.song_service import SongService
from app.schemas.song_schema import SongSchema
from app.utils.validators import validate_song_data

song_ns = Namespace('songs', description='Song operations')

song_model = song_ns.model('Song', {
    'title': fields.String(required=True, description='Song title'),
    'singer_id': fields.Integer(required=True, description='Singer ID')
})


class SongResource(Resource):
    def get(self):
        return SongService().get_all_songs()

    @song_ns.expect(song_model)
    def post(self):
        data = song_ns.payload
        errors = validate_song_data(data)
        if errors:
            return {'message': 'Validation errors', 'errors': errors}, 400
        return SongService().create_song(data)


class SongDetailResource(Resource):
    def get(self, song_id):
        song = SongService().get_song_by_id(song_id)
        if song:
            return song
        return {'message': 'Song not found'}, 404

    @song_ns.expect(song_model)
    def put(self, song_id):
        data = song_ns.payload
        errors = validate_song_data(data)
        if errors:
            return {'message': 'Validation errors', 'errors': errors}, 400
        return SongService().update_song(song_id, data)

    def delete(self, song_id):
        result = SongService().delete_song(song_id)
        if result:
            return {'message': 'Song deleted successfully'}
        return {'message': 'Song not found'}, 404


song_ns.add_resource(SongResource, '/')
song_ns.add_resource(SongDetailResource, '/<int:song_id>')
