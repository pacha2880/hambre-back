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

category_dish_association = db.Table('category_dish_association',
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
    db.Column('dish_id', db.Integer, db.ForeignKey('dish.id'), primary_key=True)
)

category_restaurant_association = db.Table('category_restaurant_association',
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.id'), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    likes = db.relationship('Like', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def get_data(self):
        return {'id': self.id, 'username': self.username, 'liked_dishes': [like.dish.get_data() for like in self.likes]}

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    
    def get_data(self):
        return {'id': self.id, 'content': self.content, 'username': self.user.username, 'dish': self.dish.name}

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    dishes = db.relationship('Dish', secondary=category_dish_association, lazy='subquery',
        backref=db.backref('categories', lazy=True))
    restaurants = db.relationship('Restaurant', secondary=category_restaurant_association, lazy='subquery',
        backref=db.backref('categories', lazy=True))
    
    def get_data(self, with_dishes=True, with_restaurants=True):
        data = {'id': self.id, 'name': self.name}
        if with_dishes:
            data['dishes'] = [dish.get_data(with_comments=False, with_categories=False) for dish in self.dishes]
        if with_restaurants:
            data['restaurants'] = [restaurant.get_data(with_dishes=False, with_categories=False) for restaurant in self.restaurants]
        return data

    @staticmethod
    def add_category(name):
        if not Category.query.filter_by(name=name).first():
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            return category
        else:
            return Category.query.filter_by(name=name).first()

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

    def get_data(self, with_dishes=True, with_categories=True):
        data = {'id': self.id, 'name': self.name, 'description': self.description, 'latitude': self.latitude, 'longitude': self.longitude}
        if with_dishes:
            data['dishes'] = [dish.get_data(with_comments=False, with_categories=False) for dish in self.dishes]
        if with_categories:
            data['categories'] = [category.get_data(with_dishes=False, with_restaurants=False) for category in self.categories]
        image_b64 = base64.b64encode(self.image).decode('ascii')
        data['image'] = image_b64
        return data

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    likes = db.relationship('Like', backref='dish', lazy=True)
    comments = db.relationship('Comment', backref='dish', lazy=True)

    def get_data(self, with_comments=True, with_categories=True):
        data = {'id': self.id, 'name': self.name, 'description': self.description, 'price': self.price, 'restaurant': self.restaurant.name}
        if with_comments:
            data['comments'] = [comment.get_data() for comment in self.comments]
        if with_categories:
            data['categories'] = [category.get_data(with_dishes=False, with_restaurants=False) for category in self.categories]
        image_b64 = base64.b64encode(self.image).decode('ascii')
        data['image'] = image_b64
        return data
        
    def like(self, username):
        user = User.query.filter_by(username=username).first()
        if user and not Like.query.filter_by(user=user, dish=self).first():
            like = Like(user=user, dish=self)
            db.session.add(like)
            db.session.commit()
            return True
        else:
            return False

    def comment(self, username, comment):
        user = User.query.filter_by(username=username).first()
        if user:
            comment = Comment(content=comment, user=user, dish=self)
            db.session.add(comment)
            db.session.commit()
            return True
        else:
            return False

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(100), nullable=False)
    # date = db.Column(db.Date, nullable=False)
    dishes = db.relationship('Dish', secondary=session_dish_association,
                                backref=db.backref('sessions', lazy='dynamic'))
    
    restaurants = db.relationship('Restaurant', secondary=session_restaurant_association,
                                backref=db.backref('sessions', lazy='dynamic'))
    
    def next_unrelated_dish(self):
        unrelated_dishes = Dish.query.filter(~Dish.sessions.contains(self)).all()
        if unrelated_dishes:
            dish = choice(unrelated_dishes)
            self.add_dish(dish)
            return dish
        else:
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
    # db.drop_all()
    db.create_all()