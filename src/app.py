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
from models import db, User, Planets, People, FavoritePlanets, FavoritePeople
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

@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))
    return jsonify(all_people)

@app.route("/people",methods=['POST'])
def add_people():
    body = request.json
    people = People(name=body["name"],birth_year=body["birth_year"],gender=body["gender"],height=body["height"], hair_color=body["hair_color"],
                    pic_url=body["pic_url"],homeworld=body["homeworld"])
    db.session.add(people)
    db.session.commit()
    print('People to add:',list(People.query.all()))
    response = {"Added":body["name"]}
    return jsonify(response)
    

@app.route('/people/<int:people_id>',methods=['GET'])
def get_single_people(people_id):
    single_people_tuple = db.session.execute(db.select(People).filter_by(id=people_id)).one_or_none()
    if single_people_tuple == None:
        return jsonify({"Message":"Not found"}),400
    single_people=single_people_tuple[0]
    return jsonify(single_people.serialize())
    

@app.route('/planets',methods=['POST'])
def post_planets():
    body = request.json
    planet = Planets(planet_name=body["planet_name"],population=body["population"],climate=body["climate"],diameter=body["diameter"], gravity=body["gravity"])
    db.session.add(planet)
    db.session.commit()
    print('Planet to add:',list(Planets.query.all()))
    return {"messaje":"Planet Added"}
    

@app.route('/planets',methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))
    return jsonify(all_planets)
    

@app.route('/planets/<int:planet_id>',methods=['GET'])
def get_single_planet(planet_id):
    single_planet_tuple = db.session.execute(db.select(Planets).filter_by(id=planet_id)).one_or_none()
    if single_planet_tuple == None:
        return jsonify({"Message":"Not found"}),400
    single_planet=single_planet_tuple[0]
    return jsonify(single_planet.serialize())


@app.route('/users',methods=['POST'])
def add_user():
    body = request.json
    print("ejecutando post")
    user = User(email=body["email"],password=body["password"],name=body["name"],is_active=True)
    db.session.add(user)
    db.session.commit()
    print('User to add:',list(User.query.all()))
    return {"messaje":"User Added"}
    

@app.route('/users',methods=['GET'])
def get_users():
    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))
    return jsonify(all_users)

@app.route('/users/favorites',methods=['GET'])
def get_current_usr_favs():
    pass

@app.route('/favorite/planet/<int:planet_id>',methods=['POST'])
def add_fav_planet(planet_id):
    body = request.json
    planet_fav = FavoritePlanets(planet_fav_id=planet_id, user_fav_id= int(body['user_id']),)
    db.session.add(planet_fav)
    db.session.commit()
    return {
        "This is the planet id" : planet_id,
        "This is the user id" : body['user_id']
    }
    

@app.route('/favorite/people/<int:people_id>',methods=['POST'])
def add_fav_people(people_id):
    body = request.json
    people_fav = FavoritePeople(people_fav_id= people_id, user_fav_id= int(body['user_id']),)
    db.session.add(people_fav)
    db.session.commit()
    return jsonify({
        "This is the people id" : people_id,
        "This is the user id" : body['user_id']
    }),200


@app.route('/favorite/planet/<int:planet_id>',methods=['DELETE'])
def delete_fav_planet():
    pass

@app.route('/favorite/people/<int:people_id>',methods=['DELETE'])
def delete_fav_people():
    pass

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
