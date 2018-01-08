import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired 
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField, validators
from wtforms.validators import Required, Length, Email, Regexp, EqualTo


class SearchForm(FlaskForm):
    search = StringField("Type in your dream", validators = [Required(message='Please type in what would you like to find')])
    submit = SubmitField("Submit")
    
