from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define association table for favorite planets and people
favorite_association = Table(
    'favorite_association',
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id')),
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    planet_favorites = relationship("Planet", secondary=favorite_association, back_populates="users")
    people_favorites = relationship("People", secondary=favorite_association, back_populates="users")

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "planet_favorites": [planet.serialize() for planet in self.planet_favorites],
            "people_favorites": [people.serialize() for people in self.people_favorites]
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    users = relationship("User", secondary=favorite_association, back_populates="people_favorites")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "gender": self.gender
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    users = relationship("User", secondary=favorite_association, back_populates="planet_favorites")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain
        }
