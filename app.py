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
from urllib.parse import quote_plus, urlencode

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/*": {"origins": "*"}})

  oauth = OAuth(app)
  

  @app.route('/')
  def get_main():
    LOGIN_URL = create_login_url()
    return render_template('index.html', session=session.get("user"), LOGIN_URL = LOGIN_URL)
  
  @app.route("/callback", methods=["GET", "POST"])
  def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")
  
  @app.route("/login")
  def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )
  
  @app.route("/logout")
  def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

  
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
  
  @app.route("/logout")
  def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

  return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)