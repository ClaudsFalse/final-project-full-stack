"""Python Flask WebApp Auth0 integration example
"""
import os
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from backend.models import Artist, Venue, Gig, setup_db, db_drop_and_create_all, db
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, abort, jsonify, request, flash
from backend.auth.auth import AuthError, requires_auth, verify_decode_jwt
from backend.utils import is_manager, is_token_expired
from flask_migrate import Migrate
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


def create_app(test_config=None):
  app = Flask(__name__)
  app.secret_key = env.get("APP_SECRET_KEY")

  setup_db(app)
  # migrate = Migrate(app, db)
  # db_drop_and_create_all()

  oauth = OAuth(app)

  oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
  )


  # Controllers API
  @app.route("/")
  def home():
    print("No active user session detected. Please login")
    if not session:
        return render_template(
            "index.html")
    else:
        print("User has logged in")
        print("session: ", session)
        token = session['user']['access_token']
        print("this is the user access token: ", token)
        if is_token_expired(token):
            return redirect('/logout')
        return redirect("/gigs")


  @app.route("/callback", methods=["GET", "POST"])
  def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/gigs")


  @app.route("/login")
  def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True),
        audience=env.get('API_AUDIENCE')
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

  @app.route('/venues')
  def get_venues():
    token = session['user']['access_token']
    try:
        venue_query = Venue.query.all()
        venues = [venue for venue in venue_query]
    except:
        abort(404)
    return render_template('venues.html', venues=venues, is_manager=is_manager(token=token))


  @app.route('/artists')
  def get_artists():
    try:
        artist_query = Artist.query.all()
        artists = [artist for artist in artist_query]
    except:
        abort(404)
    return render_template('artists.html', artists=artists)


  @app.route('/gigs')
  def get_gigs():
    if session:
        token = session['user']['access_token']
    try:
        gig_query = Gig.query.all()
    except ValueError as e:
        print(e)
    gig_data = []
    for gig in gig_query:
        venue = Venue.query.filter(Venue.id == gig.venue_id).one_or_none()
        gig_data.append(

            {"gig_id": gig.id,
             "venue_id": gig.venue_id,
             "venue_name": venue.name,
             "artist_id": gig.artist_id,
             "venue_image_link": venue.image_link,
             "start_time": gig.time,
             "hourly_rate": round(gig.hourly_rate),
             "duration": gig.duration,
             "is_booked": gig.is_booked
             })
    return render_template('gigs.html', is_manager=is_manager(token=token), gigs=gig_data)


  @app.route('/gigs', methods=['POST'])
  @requires_auth('post:gigs')
  def post_gig(payload):
    return jsonify({
        'success': True,
    })


  @app.route('/gigs/delete', methods=['POST'])
  @requires_auth('delete:gigs')
  def delete_gigs(payload):
    gig_id = request.json.get('id')
    try:
        gig = Gig.query.get_or_404(gig_id)
        db.session.delete(gig)
        db.session.commit()
    except ValueError as e:
        print(e)
    return jsonify({'message': 'Gig deleted'})


  @app.route('/gigs/<int:gig_id>/edit', methods=['GET', 'POST'])
  def edit_gig(gig_id):

    if request.method == 'GET':
        gig = Gig.query.get_or_404(gig_id)
        venue = Venue.query.get_or_404(gig.venue_id)
        gig_data = {
            'id': gig_id,
            'place': venue.name,
            'start_time': gig.time,
            'hourly_rate': gig.hourly_rate,
            'duration': gig.duration
        }
        return render_template('edit_gig.html', gig_data=gig_data)

    if request.method == 'POST':
        gig = Gig.query.get(gig_id)
        data = {
            'place': request.form.get('place'),
            'start_time': request.form.get('time'),
            'hourly_rate': request.form.get('hourly-rate'),
            'duration': request.form.get('duration')
        }
        print("*** THIS IS DATA, ", data)
        gig.start_time = data['start_time']
        gig.hourly_rate = data['hourly_rate']
        gig.duration = data['duration']
        db.session.commit()
        db.session.close()
        flash("Gig updated successfully")
        return redirect('/gigs')


  @app.route('/gigs/create', methods=['GET', 'POST'])
  def create_gigs():
    if request.method == 'POST':
        data = {
            'place': request.form.get('place'),
            'start_time': request.form.get('time'),
            'hourly_rate': request.form.get('hourly-rate'),
            'duration': request.form.get('duration')
        }

        # get the venue id
        try:
            venue_query = Venue.query.filter(
                Venue.name == data['place']).one_or_none()

            newGig = Gig(
                venue_id=venue_query.id,
                artist_id=None,
                time=request.form.get('time'),
                hourly_rate=request.form.get('hourly-rate'),
                duration=request.form.get('duration'),
                is_booked=False
            )

            db.session.add(newGig)
            db.session.commit()
            db.session.close()

        except ValueError as e:
            print(e)
        return redirect('/gigs')
    else:
        return render_template('new_gig.html')
  return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
