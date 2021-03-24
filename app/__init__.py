from flask import Flask
from .config import Config


UPLOAD_FOLDER = './app/static/uploads'
SECRET_KEY='secret'

app = Flask(__name__)
app.config.from_object(Config)

from app import views