import base64
import io
import os
from PIL import Image
from flask import Flask, jsonify, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from random import choice

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


session_dish_association = db.Table('session_dish_association',
    db.Column('session_id', db.Integer, db.ForeignKey('session.id'), primary_key=True),
    db.Column('dish_id', db.Integer, db.ForeignKey('dish.id'), primary_key=True)
)

session_restaurant_association = db.Table('session_restaurant_association',
    db.Column('session_id', db.Integer, db.ForeignKey('session.id'), primary_key=True),
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.id'), primary_key=True)
)

# create restaurant model that has one to many relation with dishes it has name, description, latutude, longitude, image
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float(precision=15), nullable=False)
    longitude = db.Column(db.Float(precision=15), nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)
    dishes = db.relationship('Dish', backref='restaurant', lazy=True)

    def add_dish(self, name, description, price, image):
        dish = Dish(name=name, description=description, price=price, image=image, restaurant=self)
        db.session.add(dish)
        db.session.commit()
        
    def get_data(self):
        image_b64 = base64.b64encode(self.image).decode('ascii')
        return {'id': self.id, 'name': self.name, 'description': self.description,
                'latitude': self.latitude, 'longitude': self.longitude, 'image': image_b64}
        

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

    def get_data(self):
        image_b64 = base64.b64encode(self.image).decode('ascii')
        return {'id': self.id, 'name': self.name, 'description': self.description,
                'price': self.price, 'restaurant_name': self.restaurant.name,
                'restaurant_id': self.restaurant_id, 'image': image_b64}

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(100), nullable=False)
    # date = db.Column(db.Date, nullable=False)
    dishes = db.relationship('Dish', secondary=session_dish_association,
                                backref=db.backref('sessions', lazy='dynamic'))
    
    restaurants = db.relationship('Restaurant', secondary=session_restaurant_association,
                                backref=db.backref('sessions', lazy='dynamic'))
    
    def next_unrelated_dish(self):
        # get all dishes that are not related to the session
        unrelated_dishes = Dish.query.filter(~Dish.sessions.contains(self)).all()
        if unrelated_dishes:
            # if there are unrelated dishes, return a random one
            dish = choice(unrelated_dishes)
            self.add_dish(dish)
            return dish
        else:
            # if all dishes are already related, end all relations and start again
            self.dishes.clear()
            db.session.commit()
            return self.next_unrelated_dish()

    def next_unrelated_restaurant(self):
        unrelated_restaurants = Restaurant.query.filter(~Restaurant.sessions.contains(self)).all()
        if unrelated_restaurants:
            restaurant = choice(unrelated_restaurants)
            self.add_restaurant(restaurant)
            return restaurant
        else:
            self.restaurants.clear()
            db.session.commit()
            return self.next_unrelated_restaurant()
    
    def add_dish(self, dish):
        if dish not in self.dishes:
            self.dishes.append(dish)
            db.session.commit()
            
    def add_restaurant(self, restaurant):
        if restaurant not in self.restaurants:
            self.restaurants.append(restaurant)
            db.session.commit()

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/dishes', methods=['GET'])
def get_dishes():
    dishes = Dish.query.all()
    output = []
    for dish in dishes:
        output.append(dish.get_data())
    return jsonify(output)

@app.route('/dishes/<int:id>', methods=['GET'])
def get_dish(id):
    dish = Dish.query.get_or_404(id)
    return jsonify(dish.get_data())

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    output = []
    for restaurant in restaurants:
        output.append(restaurant.get_data())
    return jsonify(output)

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    return jsonify(restaurant.get_data())

@app.route('/restaurants/<int:id>/dishes', methods=['GET'])
def get_restaurant_dishes(id):
    restaurant = Restaurant.query.get_or_404(id)
    output = []
    for dish in restaurant.dishes:
        output.append(dish.get_data())
    return jsonify(output)

@app.route('/sessions/<int:session_id>/next_dish', methods=['GET'])
def next_dish(session_id):
    session = Session.query.get(session_id)
    if not session:
        session = Session(id=session_id)
        db.session.add(session)
        db.session.commit()
    dish = session.next_unrelated_dish()
    return jsonify(dish.get_data())

@app.route('/sessions/<int:session_id>/next_restaurant', methods=['GET'])
def next_restaurant(session_id):
    session = Session.query.get(session_id)
    if not session:
        session = Session(id=session_id)
        db.session.add(session)
        db.session.commit()
    restaurant = session.next_unrelated_restaurant()
    return jsonify(restaurant.get_data())

def read_image_bytes(folder, image_name):
    image_path = folder + image_name
    if not os.path.exists(image_path + '.jpg'):
        with open(image_path + '.png', 'rb') as f:
            img_data = f.read()
        img = Image.open(io.BytesIO(img_data))
        img = img.convert('RGB')
        img.save(image_path + '.jpg', optimize=True, quality=50)
    with open(image_path + '.jpg', 'rb') as f:
        img_bytes = f.read()
    return img_bytes


def load_restaurants():
    restaurant_images = os.listdir('base_data/restaurants')
    # print(restaurant_images)
    for restaurant_image in restaurant_images:
        if(restaurant_image[-4:] != '.png'):
            continue
        file_name = restaurant_image[:-4]
        restaurant_data = file_name.split('_')
        # print(restaurant_data)
        restaurant_name = restaurant_data[0]
        restaurant_latitude = float(restaurant_data[1])
        restaurant_longitude = float(restaurant_data[2])
        restaurant_description = restaurant_description = 'El restaurante ' + restaurant_name + ' es ' + choice(['de las mejores opciones', 'de las mejores alternativas', 'de las mejores opciones', 'de las mejores alternativas', 'de las mejores alternativas', 'de las mejores opciones', 'de las mejores opciones', 'de las mejores opciones', 'de las mejores alternativas', 'de las mejores alternativas', 'de las mejores opciones'])
        restaurant_image_bytes = read_image_bytes('base_data/restaurants/', file_name)
        restaurant = Restaurant(name=restaurant_name, description=restaurant_description, latitude=restaurant_latitude, longitude=restaurant_longitude, image=restaurant_image_bytes)
        db.session.add(restaurant)
        db.session.commit()

def load_dishes():
    dish_images = os.listdir('base_data/dishes')
    for dish_image in dish_images:
        file_name = dish_image[:-4]
        dish_data = file_name.split('_')
        # print(dish_data)
        restaurant_name = dish_data[0]
        # print('#' * 50)
        # print(restaurant_name)
        # print('#' * 50)
        # print(Restaurant.query.filter_by(name=restaurant_name).first())
        restaurant_id = Restaurant.query.filter_by(name=restaurant_name).first().id
        # get dish name from image name
        dish_name = dish_data[1]
        # get dish data from json file
        dish_price = int(dish_data[2])
        dish_image_bytes = read_image_bytes('base_data/dishes/', file_name)
        # generate a random food description in base of the name in spanish
        dish_description = 'Un ' + dish_name + ' ' + choice(['rico', 'delicioso', 'sabroso', 'exquisito', 'deli', 'inigualable'])
        # create new dish
        dish = Dish(name=dish_name, description=dish_description, price=dish_price, image=dish_image_bytes, restaurant_id=restaurant_id)
        # add dish to the database
        db.session.add(dish)
        db.session.commit()

def load_data():
    load_restaurants()
    load_dishes()

if __name__ == '__main__':
    with app.app_context():
        restaurant1 = Restaurant(name='Caserita', description='la mejor caserita de la ciudad', latitude=-17.3935451, longitude=-66.1487274, image=read_image_bytes('images/', 'caserita'))
        
        # create new dishes
        dish1 = Dish(name='Silpancho', description='Un silpanchito', price=17, image=read_image_bytes('images/', 'silpancho'), restaurant=restaurant1)
        dish2 = Dish(name='Trancapecho', description='Es un silpancho en pan :v', price=12, image=read_image_bytes('images/', 'trancapecho'), restaurant=restaurant1)
        dish3 = Dish(name='Salchipapa', description='Papas fritas con papas nmms', price=18.99, image=read_image_bytes('images/','salchipapa'), restaurant=restaurant1)

        # add dishes to the database
        db.session.add(restaurant1)
        db.session.add(dish1)
        db.session.add(dish2)
        db.session.add(dish3)
        db.session.commit()        

        load_data()

    app.run(debug=True)

