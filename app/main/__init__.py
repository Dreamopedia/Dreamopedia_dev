import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views