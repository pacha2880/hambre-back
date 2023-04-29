from app import app
from utils.utils import load_data


with app.app_context(): 
    load_data()
