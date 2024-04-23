#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

from flask import Flask, jsonify, request
from models import Hero, Power, HeroPower

app = Flask(__name__)

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    serialized_heroes = [hero.to_dict() for hero in heroes]
    return jsonify(serialized_heroes)

# GET /heroes/:id
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict())
    else:
        return jsonify({'error': 'Hero not found'}), 404

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    serialized_powers = [power.to_dict() for power in powers]
    return jsonify(serialized_powers)

# GET /powers/:id
@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.to_dict())
    else:
        return jsonify({'error': 'Power not found'}), 404

# PATCH /powers/:id
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power:
        data = request.get_json()
        if 'description' in data:
            power.description = data['description']
            db.session.commit()
            return jsonify(power.to_dict())
        else:
            return jsonify({'error': 'Invalid request. Description is required.'}), 400
    else:
        return jsonify({'error': 'Power not found'}), 404

# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    if hero_id is None or power_id is None:
        return jsonify({'error': 'Hero ID and Power ID are required.'}), 400

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if hero is None:
        return jsonify({'error': 'Hero not found'}), 404

    if power is None:
        return jsonify({'error': 'Power not found'}), 404

    hero_power = HeroPower(hero=hero, power=power, strength=strength)
    db.session.add(hero_power)
    db.session.commit()

    return jsonify(hero_power.to_dict())


if __name__ == '__main__':
    app.run(port=5555, debug=True)
