"""Python Flask WebApp Auth0 integration example
"""
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from backend.models import Artist, Venue, Gig, setup_db, db_drop_and_create_all, db
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, abort, jsonify, request
from backend.auth.auth import AuthError, requires_auth, verify_decode_jwt
from backend.utils import is_manager
from flask_migrate import Migrate

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

setup_db(app)
#migrate = Migrate(app, db) 
#db_drop_and_create_all()

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
    return render_template(
        "index.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    print(token['access_token'])
    session["user"] = token
    return redirect("/")


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

@app.route('/gigs')
def get_gigs():
  token=session['user']['access_token']
  try:
    print("try")
    gig_query= Gig.query.all()
    print("gig query: ", gig_query)
  except ValueError as e:
     print(e)
  gig_data = []
  for gig in gig_query:
    print("venue_id", gig.venue_id)
    venue = Venue.query.filter(Venue.id==gig.venue_id).one_or_none()
    gig_data.append(
       {
              "venue_id":gig.venue_id,
              "venue_name":venue.name,
              "artist_id":gig.artist_id,
              "venue_image_link":venue.image_link,
              "start_time": gig.time,
              "hourly_rate": gig.hourly_rate,
              "duration":gig.duration,
              "is_booked":gig.is_booked
        })
    print("GIG DATA", gig_data)
  return render_template('gigs.html', is_manager=is_manager(token=token), gigs=gig_data)
  
  

   
   

@app.route('/gigs', methods=['POST'])
@requires_auth('post:gigs')
def post_gig(payload):
  return jsonify({
            'success': True, 
    })

@app.route('/gigs/create', methods=['GET', 'POST'])
def create_gigs():
  if request.method == 'POST':
        data = {
        'place': request.form.get('place'),
        'start_time': request.form.get('time'),
        'hourly_rate': request.form.get('hourly-rate'),
        'duration': request.form.get('duration')
        }

        print(data)

        #get the venue id
        try:
          venue_query = Venue.query.filter(Venue.name == data['place']).one_or_none()
          print(venue_query.name)
          print(venue_query.id)

          newGig = Gig(
             venue_id = venue_query.id,
             artist_id = None,
             time = request.form.get('time'),
             hourly_rate = request.form.get('hourly-rate'),
             duration = request.form.get('duration'),
             is_booked = False
          )

          db.session.add(newGig)
          db.session.commit()
         
        except ValueError as e:
           print(e)
        return redirect('/gigs')
  else:
    return render_template('new_gig.html')


if __name__ == "__main__":
    app.run(debug=True)
