
import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Artist
Have title and release year
'''
class Venue(db.Model):
    __tablename__ = 'venues'

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    name = Column(db.String)
    genres = Column(db.ARRAY(db.String), nullable=False)
    # city = Column(db.String(120))
    # state = Column(db.String(120))
    address = Column(db.String(120))
    phone = Column(db.String(120))
    # website = Column(db.String(500))
    image_link = Column(db.String(500))
    # facebook_link = db.Column(db.String(120))
    # seeking_talent = db.Column(db.Boolean)
    # seeking_description = db.Column(db.String(500))
    productions = db.relationship('Production', backref='venue', lazy='joined', cascade="all, delete")

class Artist(db.Model):
    __tablename__ = 'artists'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    # city = Column(db.String(120))
    # state = Column(db.String(120))
    phone = Column(db.String(120))
    genres = Column(db.ARRAY(db.String), nullable=False)
    # image_link = db.Column(db.String(500))
    # facebook_link = db.Column(db.String(120))
    # seeking_venue= db.Column(db.Boolean)
    # website = db.Column(db.String(500))
    # seeking_description = db.Column(db.String(500))
    productions = db.relationship('Production', backref='artist', lazy='joined', cascade="all, delete")

class Production(db.Model):
  __tablename__ = 'productions'
  id = Column(db.Integer, primary_key=True)
  # define foreign keys that map to the primary keys in the respective parent tables
  venue_id = Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
  artist_id = Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
