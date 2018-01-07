import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import flask_whooshalchemy as whooshalchemy
from whoosh.analysis import StemmingAnalyzer
from config import config

boostrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    boostrap.init_app(app)
    
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    #add here other blueprints to run
    return app