from flask import Flask
from .config import get_config
from .extensions import db, migrate
from flask_restx import Api
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    register_loggers(app)
    register_exts(app)
    register_namespaces(app)
    return app


def register_exts(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_loggers(app):
    app.logger.setLevel(logging.INFO)
    handler = logging.FileHandler(app.config['LOG_FILE'])
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

def register_namespaces(app):
    api = Api(
        app,
        title="Music API",
        version="1.0",
        description="简单的 Music API",
        doc="/docs"
    )
    from .api.namespaces.singer_ns import singer_ns
    from .api.namespaces.song_ns import song_ns
    api.add_namespace(singer_ns)
    api.add_namespace(song_ns)
