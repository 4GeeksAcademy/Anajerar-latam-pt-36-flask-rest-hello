from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(80),nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    # Relationship to Favorite planets
    user_fav_planet = db.relationship('FavoritePlanets',back_populates='user')

    # Relationshio to Favorite people
    user_fav_people = db.relationship('FavoritePeople', back_populates='user')

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        fav_planets_serialized = []
        for fav_planets_list in self.user_fav_planet:
            fav_planets_serialized.append(fav_planets_list.serialize())

        fav_people_serialized = []
        for fav_people_list in self.user_fav_people:
            fav_people_serialized.append(fav_people_list.serialize())

        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "is_active": self.is_active,
            "fav planets" : fav_planets_serialized,
            "fav_people" : fav_people_serialized
            # do not serialize the password, its a security breach
        }
     
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(50), unique=True, nullable=False)
    population = db.Column(db.Integer)
    climate = db.Column(db.String(25))
    diameter = db.Column(db.Integer)
    gravity = db.Column(db.Integer)

    # Planets to People relationship
    people = db.relationship('People', back_populates="planet")

    # Planets to favs relationship
    favs = db.relationship('FavoritePlanets', back_populates='planet' )

    def __repr__(self):
        return '<Planet %r>' % self.planet_name
    
    def serialize(self):
        people_in_planet_serialized = []
        for people_in_planet in self.people:
            people_in_planet_serialized.append(people_in_planet.serialize())

        return {
            "id": self.id,
            "planet_name": self.planet_name,
            "population": self.population,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "people_in_planet" : people_in_planet_serialized   
        }
        
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    birth_year = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(10))
    height = db.Column(db.String(10))
    hair_color = db.Column(db.String(10))
    pic_url = db.Column(db.String(100))
    homeworld = db.Column(db.Integer,db.ForeignKey(Planets.id))

    # Relationship to planets
    planet = db.relationship(Planets, back_populates="people")

    # Relationship to favorite people
    user_fav_people = db.relationship('FavoritePeople', back_populates='people')

    def __init__(self,name,birth_year,gender,height,hair_color,pic_url,homeworld):
        self.name = name
        self.birth_year = birth_year
        self.gender = gender
        self.height = height
        self.hair_color = hair_color
        self.pic_url = pic_url
        self.homeworld = homeworld

    def __repr__(self):
        return '<People %r>' % self.name
    
    def serialize(self):
        return {
            "Name" : self.name,
            "Birth_year" : self.birth_year,
            "Gender" : self.gender,
            "Height" : self.height,
            "Picture URL" : self.pic_url,
            "Homeworld": self.homeworld
        }
        
class FavoritePlanets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_fav_id = db.Column(db.Integer, db.ForeignKey(Planets.id))
    user_fav_id = db.Column(db.Integer, db.ForeignKey(User.id))

    # Relationship to users
    user = db.relationship(User, back_populates='user_fav_planet')

    # Relationship to planets
    planet = db.relationship(Planets, back_populates='favs')

    def __init__(self, planet_fav_id, user_fav_id):
        self.planet_fav_id = planet_fav_id
        self.user_fav_id = user_fav_id

    def __repr__(self):
        return '<Favs %r>' % self.id
    
    def serialize(self):
        return {
            "id" : self.id,
            "Planet fav" : self.planet_fav_id,
            "user_fav_id" : self.user_fav_id
        }

class FavoritePeople(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    people_fav_id = db.Column(db.Integer, db.ForeignKey(People.id))
    user_fav_id = db.Column(db.Integer,db.ForeignKey(User.id))

    # Relationship to user
    user = db.relationship(User, back_populates = 'user_fav_people')

    # Relationship to People
    people = db.relationship(People, back_populates = 'user_fav_people')

    def __init__(self, people_fav_id, user_fav_id):
        self.people_fav_id = people_fav_id
        self.user_fav_id = user_fav_id

    def __repr__(self):
        return '<Favs %r>' % self.id
    
    def serialize(self):
        return {
            "id" : self.id,
            "People fav" : self.people_fav_id,
            "user_fav_id" : self.user_fav_id
        }

