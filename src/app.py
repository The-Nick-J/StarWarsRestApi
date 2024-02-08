"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet
#from models import Person



app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200
#ENDPOINTS DE PEOPLE
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all() # [<Note 1>, <Note 2>]
    print(people)
    people = list(map(lambda people: people.serialize(), people))
    print(people) 
    return jsonify(people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    people = People.query.get(people_id) # [<Note 1>, <Note 2>]
    if people is None:
        return jsonify({'error': 'Person not found'}), 404
    serialized_person = people.serialize()
    return jsonify(serialized_person), 200

@app.route('/people', methods=["POST"])
def add_people():
    data = request.json
    name = data.get('name')
    height = data.get('height')
    gender = data.get('gender')
    people = People(name=name, height=height, gender=gender)
    db.session.add(people) 
    db.session.commit()

    return jsonify({"message": "People added successfully"}), 201

#/ENDPOINTS DE PEOPLE


#ENDPOINTS DE PLANETS
@app.route('/planets', methods=['GET'])
def get_planets():
    planet = Planet.query.all() # [<Note 1>, <Note 2>]
    print(planet)
    planet = list(map(lambda planet: planet.serialize(), planet))
    print(planet) 
    return jsonify(planet), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    planet = Planet.query.get(planet_id) # [<Note 1>, <Note 2>]
    if planet is None:
        return jsonify({'error': 'Planet not found'}), 404
    serialized_planet = planet.serialize()
    return jsonify(serialized_planet), 200

@app.route('/planets', methods=["POST"])
def add_planet():
    data = request.json
    name = data.get('name')
    climate = data.get('climate')
    terrain = data.get('terrain')
    planet = Planet(name=name, climate=climate, terrain=terrain)
    db.session.add(planet) 
    db.session.commit()

    return jsonify({"message": "Planet added successfully"}), 201



    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
