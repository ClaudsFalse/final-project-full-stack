import os
import json
from flask import (
    Flask, 
    abort,
    render_template, 
    session,
    flash, 
    redirect, 
    url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from backend.models import setup_db, Artist, Venue, db, db_drop_and_create_all
from authlib.integrations.flask_client import OAuth
from backend.auth.auth import AuthError, requires_auth
from backend.utils import *
from urllib.parse import quote_plus, urlencode

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  migrate = Migrate(app, db)
  db_drop_and_create_all()

  # ROUTES
  app.app_context().push()
  CORS(app, resources={r"/*": {"origins": "*"}})
  app.secret_key = env.get("APP_SECRET_KEY")

  oauth = OAuth(app)

  oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
    )


  @app.route("/")
  def home():
    data=session.get('user')

    return render_template("index.html", 
                           session=data,
                           pretty=json.dumps(session.get('user'),
                                             indent=4))

  
  @app.route("/login")
  def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )
  
  @app.route("/callback", methods=["GET", "POST"])
  def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")
  
  @app.route("/logout")
  def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )
  
  @app.route("/account")
  def get_user_account():
    data=session.get('user')
    if session:
      email = data['userinfo']['email']
      artist = Artist.query.filter(Artist.email == email).one_or_none()
      if artist:
        return render_template('view_artist_account.html', name=artist.name)
      else:
        return render_template('create_account.html')
   

  @app.route('/productions')
  def get_productions():
    return render_template('productions.html')
  
  @app.route('/venues')
  def get_venues():
    try:
      venue_query = Venue.query.all()
      venues = [venue for venue in venue_query]
    except:
      abort(404)
    return render_template('venues.html', venues=venues)
  
  @app.route('/artists')
  def get_artists():
    try:
      artist_query = Artist.query.all()
      artists = [artist for artist in artist_query]
    except:
      abort(404)
    return render_template('artists.html', artists=artists)
  
  return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)