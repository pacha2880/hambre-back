from app import app
from utils.utils import load_data

print("asdfasdf" * 100)
with app.app_context(): 
    load_data()
