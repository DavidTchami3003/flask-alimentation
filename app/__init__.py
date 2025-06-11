from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db=SQLAlchemy()


def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .models import init_models
    init_models()

    from .routes import init_routes
    init_routes(app)

    return app