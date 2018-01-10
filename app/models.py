import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from app import db
from whoosh.analysis import StemmingAnalyzer
import flask_whooshalchemy as whooshalchemy

class Dream(db.Model):
    
    __tablename__ = 'dreams'
    __searchable__ = ['name', 'description']
    __analyzer__ = StemmingAnalyzer()
    
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    
    def __repr__(self):
        return '<Dream %r>' %self.name
