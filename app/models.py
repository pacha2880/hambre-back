import base64
from random import choice
from flask_sqlalchemy import SQLAlchemy
from app import app

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