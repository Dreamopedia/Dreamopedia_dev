import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from app import create_app, db
from app.models import Dream 
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import flask.ext.whooshalchemy as whooshalchemy
from config import config


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)
with app.app_context():
    whooshalchemy.whoosh_index(app, Dream)

def make_shell_context():
    return dict(app=app, db=db, Dream=Dream)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
 manager.run()