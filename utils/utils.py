import io
import os
from random import choice
from PIL import Image

from app.models import Category, Dish, Restaurant
from app.models import db

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


def random_categories():
    categories = ['Arepas', 'Asiática', 'Bebidas', 'Café', 'Carnes', 'Cervezas', 'Chatarra', 'Comida rápida', 'Desayunos', 'Ensaladas', 'Helados', 'Hamburguesas', 'Italiana', 'Jugos', 'Mariscos', 'Mexicana', 'Parrilla', 'Pastas', 'Pizzas', 'Postres', 'Sándwiches', 'Sopas', 'Sushi', 'Tacos', 'Té', 'Vegana', 'Vegetariana']
    random_categories = []
    while len(random_categories) < 3:
        random_category = choice(categories)
        if random_category not in random_categories:
            random_categories.append(random_category)
    return random_categories

def load_restaurants():
    restaurant_images = os.listdir('base_data/restaurants')
    for restaurant_image in restaurant_images:
        if(restaurant_image[-4:] != '.png'):
            continue
        file_name = restaurant_image[:-4]
        restaurant_data = file_name.split('_')
        print(restaurant_data)
        restaurant_name = restaurant_data[0]
        if Restaurant.query.filter_by(name=restaurant_name).first():
            continue
        restaurant_latitude = float(restaurant_data[1])
        restaurant_longitude = float(restaurant_data[2])
        restaurant_description = restaurant_description = 'El restaurante ' + restaurant_name + ' es ' + choice(['de las mejores opciones', 'de las mejores alternativas', 'de las mejores opciones', 'de las mejores alternativas', 'de las mejores alternativas', 'de las mejores opciones', 'de las mejores opciones', 'de las mejores opciones', 'de las mejores alternativas', 'de las mejores alternativas', 'de las mejores opciones'])
        restaurant_image_bytes = read_image_bytes('base_data/restaurants/', file_name)
        category_names = random_categories()
        categories = []
        for category in category_names:
            categories.append(Category.add_category(category))
        restaurant = Restaurant(name=restaurant_name, description=restaurant_description,
                                latitude=restaurant_latitude, longitude=restaurant_longitude,
                                image=restaurant_image_bytes, categories=categories)
        db.session.add(restaurant)
        db.session.commit()

def load_dishes():
    dish_images = os.listdir('base_data/dishes')
    for dish_image in dish_images:
        file_name = dish_image[:-4]
        dish_data = file_name.split('_')
        print(dish_data)
        restaurant_name = dish_data[0]
        restaurant_id = Restaurant.query.filter_by(name=restaurant_name).first().id
        dish_name = dish_data[1]
        if Dish.query.filter_by(name=dish_name, restaurant_id=restaurant_id).first():
            continue
        dish_price = int(dish_data[2])
        dish_image_bytes = read_image_bytes('base_data/dishes/', file_name)
        dish_description = 'Un ' + dish_name + ' ' + choice(['rico', 'delicioso', 'sabroso', 'exquisito', 'deli', 'inigualable'])
        category_names = random_categories()
        categories = []
        for category in category_names:
            categories.append(Category.add_category(category))
        dish = Dish(name=dish_name, description=dish_description, price=dish_price, 
                    image=dish_image_bytes, restaurant_id=restaurant_id,
                    categories=categories)
        db.session.add(dish)
        db.session.commit()

def load_simple_initial_data():
    if Restaurant.query.filter_by(name='Caserita').first():
        return
    restaurant1 = Restaurant(name='Caserita', description='la mejor caserita de la ciudad', latitude=-17.3935451, longitude=-66.1487274, image=read_image_bytes('images/', 'caserita'))
    
    dish1 = Dish(name='Silpancho', description='Un silpanchito', price=17, image=read_image_bytes('images/', 'silpancho'), restaurant=restaurant1)
    dish2 = Dish(name='Trancapecho', description='Es un silpancho en pan :v', price=12, image=read_image_bytes('images/', 'trancapecho'), restaurant=restaurant1)
    dish3 = Dish(name='Salchipapa', description='Papas fritas con papas nmms', price=18.99, image=read_image_bytes('images/','salchipapa'), restaurant=restaurant1)

    db.session.add(restaurant1)
    db.session.add(dish1)
    db.session.add(dish2)
    db.session.add(dish3)
    db.session.commit()  

def load_data():
    load_simple_initial_data()
    load_restaurants()
    load_dishes()