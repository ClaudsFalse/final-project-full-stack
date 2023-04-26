from os import environ as env
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

database_path = env['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    newArtist = Artist(name = 'Jordan',
                   email = 'artist@groove.com',
                   phone = '07563489658',
                   genres = ['disco', 'house'])
    
    newVenue = Venue(name="Tabac", 
                     genres=['disco', 'house'],
                     address="Mitchell Lane",
                     phone="01415721448",
                     image_link="https://shorturl.at/vL789")
    

    items = [newArtist, newVenue]
    for item in items:
        db.session.add(item)
        db.session.commit()



'''
Artist
Have title and release year
'''
class Venue(db.Model):
    __tablename__ = 'venues'

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    name = Column(db.String)
    genres = Column(db.ARRAY(db.String), nullable=False)
    address = Column(db.String(120))
    phone = Column(db.String(120))
    image_link = Column(db.String(500))
    gigs = db.relationship('Gig', backref='venue', lazy='joined', cascade="all, delete")

class Artist(db.Model):
    __tablename__ = 'artists'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    email = Column(db.String)
    phone = Column(db.String(120))
    genres = Column(db.ARRAY(db.String), nullable=False)
    gigs = db.relationship('Gig', backref='artist', lazy='joined', cascade="all, delete")

class Gig(db.Model):
  __tablename__ = 'productions'
  id = Column(db.Integer, primary_key=True)
  # define foreign keys that map to the primary keys in the respective parent tables
  venue_id = Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
  artist_id = Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
