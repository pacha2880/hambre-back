from flask import jsonify, request, g
from app import app
from app.models import Category, Dish, Restaurant, Session, User
from app.models import db


@app.before_request
def save_location():
    if request.is_json:
        if 'latitude' in request.json and 'longitude' in request.json:
            g.latitude = request.json['latitude']
            g.longitude = request.json['longitude']
        if 'username' in request.json:
            g.username = request.json['username']

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
    return jsonify(restaurant.get_data(with_dishes=False))

@app.route('/users', methods=['POST'])
def create_user():
    username = request.json.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.get_data())

@app.route('/dishes/<int:dish_id>/like', methods=['POST'])
def like_dish(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    if dish.like(username=request.json.get('username')):
        db.session.commit()
        return jsonify({'like': 1}), 200
    else:
        return jsonify({'like': 0}), 200
    
@app.route('/dishes/<int:dish_id>/comment', methods=['POST'])
def comment_dish(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    dish.comment(username=request.json.get('username'), comment=request.json.get('comment'))
    db.session.commit()
    return jsonify({'message': 'Dish commented successfully'}), 200

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    output = []
    for category in categories:
        output.append(category.get_data(with_dishes=False, with_restaurants=False))
    return jsonify(output)