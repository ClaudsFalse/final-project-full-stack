import os
from flask import (
    Flask, 
    render_template, 
    request, 
    session,
    flash, 
    redirect, 
    url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from backend.models import setup_db
from authlib.integrations.flask_client import OAuth
from backend.auth.auth import AuthError, requires_auth
from backend.utils import *

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/*": {"origins": "*"}})

  oauth = OAuth(app)
  

  @app.route('/')
  def get_main():
    LOGIN_URL = create_login_url()
    # session = session.get("user")
    return render_template('index.html', LOGIN_URL = LOGIN_URL)
  
  # @app.route('/drinks-detail', methods=['GET'])
  # @requires_auth('get:drinks-detail')
  @app.route('/productions')
  def get_productions():
    return render_template('productions.html')
  
  @app.route('/venues')
  def get_venues():
    return render_template('venues.html')
  
  @app.route('/artists')
  def get_artists():
    return render_template('artists.html')
  
  @app.route("/login")
  def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

  return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)