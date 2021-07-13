from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()

ma = Marshmallow()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.ProductionConfig')
    db.init_app(app)

    with app.app_context():
        from . import routes

        db.create_all() 
        # creates tables and database if not all ready created
        from .models import ScrapReasons
        ScrapReasons.populate_table()
        # populates scrap reason table
        return app
