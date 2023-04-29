from flask import jsonify
from app import app
from app.models import Dish, Restaurant, Session
from app.models import db


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
    session = db.session.get(Session, session_id)
    if not session:
        session = Session(id=session_id)
        db.session.add(session)
        db.session.commit()
    dish = session.next_unrelated_dish()
    return jsonify(dish.get_data())

@app.route('/sessions/<int:session_id>/next_restaurant', methods=['GET'])
def next_restaurant(session_id):
    session = db.session.get(Session, session_id)
    if not session:
        session = Session(id=session_id)
        db.session.add(session)
        db.session.commit()
    restaurant = session.next_unrelated_restaurant()
    return jsonify(restaurant.get_data())
