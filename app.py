import base64
import io
import os
from PIL import Image
from flask import Flask, jsonify, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Dish(db.Model):
    __tablename__ = 'dishes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    # restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    # restaurant = db.relationship('Restaurant', backref=db.backref('foods', lazy=True))
    image = db.Column(db.LargeBinary, nullable=True)
    
    def __repr__(self):
        return f'<Food {self.id}: {self.name}>'

# @app.before_first_request
def setup_database():
    # drop all tables in the database
    db.drop_all()
    # create new tables based on the model classes
    db.create_all()

with app.app_context():
    db.drop_all()
    db.create_all()  # create tables based on model classes

@app.route('/dishes', methods=['GET'])
# @cross_origin()
def get_dishes():
    dishes = Dish.query.all()
    output = []
    for dish in dishes:
        dish_data = {'id': dish.id, 'name': dish.name, 'description': dish.description, 'price': dish.price, 'image': dish.image}
        output.append(dish_data)
    return jsonify({'dishes': output})

@app.route('/dishes/<int:id>', methods=['GET'])
# @cross_origin()
def get_dish(id):
    dish = Dish.query.get_or_404(id)
    image = base64.b64encode(dish.image).decode('ascii')
    dish_data = {'id': dish.id, 'name': dish.name, 'description': dish.description, 'price': dish.price, 'image': image}
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return jsonify({'dish': dish_data})

# @app.route('/dishes', methods=['POST'])
# def add_dish(name, price, image):
#     dish = Dish(name=name, price=price, image=image)
#     db.session.add(dish)
#     db.session.commit()
#     return dish.id

# @app.route('/dishes/<int:id>', methods=['PUT'])
# def update_dish(id):
#     dish = Dish.query.get_or_404(id)
#     name = request.json.get('name', dish.name)
#     description = request.json.get('description', dish.description)
#     price = request.json.get('price', dish.price)
#     dish.name = name
#     dish.description = description
#     dish.price = price
#     db.session.commit()
#     dish_data = {'id': dish.id, 'name': dish.name, 'description': dish.description, 'price': dish.price}
#     return jsonify({'dish': dish_data})

# @app.route('/dishes/<int:id>', methods=['DELETE'])
# def delete_dish(id):
#     dish = Dish.query.get_or_404(id)
#     db.session.delete(dish)
#     db.session.commit()
#     return '', 204

def read_image_bytes(image_name):
    # if image compressed .jpg doesnt exist, compress it
    print(image_name)
    image_path = 'images/' + image_name
    if not os.path.exists(image_path + '.jpg'):
        with open(image_path + '.png', 'rb') as f:
            img_data = f.read()
        img = Image.open(io.BytesIO(img_data))
        img = img.convert('RGB')
        img.save(image_path + '.jpg', optimize=True, quality=50)
    with open(image_path + '.jpg', 'rb') as f:
        img_bytes = f.read()
    return img_bytes


if __name__ == '__main__':
    with app.app_context():
        # create new dishes
        dish1 = Dish(name='Silpancho', description='Un silpanchito', price=17, image=read_image_bytes('silpancho'))
        dish2 = Dish(name='Trancapecho', description='Es un silpancho en pan :v', price=12, image=read_image_bytes('trancapecho'))
        dish3 = Dish(name='Salchipapa', description='Papas fritas con papas nmms', price=18.99, image=read_image_bytes('salchipapa'))

        # add dishes to the database
        db.session.add(dish1)
        db.session.add(dish2)
        db.session.add(dish3)
        db.session.commit()

    app.run(debug=True)

