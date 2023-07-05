from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_cors import CORS

db = SQLAlchemy()
dbName = "SDP.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abcdef'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{dbName}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/SDP'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'website/static/profile_pic'
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
    db.init_app(app)
    CORS(app)

    from .view import view
    app.register_blueprint(view, url_prefix='/')

    from .database import User, GameData, ProfileData
    create_database(app)

    return app 

def create_database(app):
    if not path.exists('website/' + dbName):
        with app.app_context():
            db.create_all()

