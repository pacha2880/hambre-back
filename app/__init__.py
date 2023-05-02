from flask import Flask
from flask_cors import CORS
from app.config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

from app import routes
