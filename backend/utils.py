from backend.auth.auth import AuthError, requires_auth, verify_decode_jwt
from jose import jwt
import jwt
import json
import requests
import datetime
from os import environ as env
from dotenv import find_dotenv, load_dotenv
from backend.models import Artist, Gig, Venue
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

def memoize(function):
  memo = {}
  def wrapper(*args):
    if args in memo:
      return memo[args]
    else:
      rv = function(*args)
      memo[args] = rv
      return rv
  return wrapper

def is_manager(token):
    decoded = verify_decode_jwt(token)
    permissions = decoded['permissions']
    if 'delete:gigs' in permissions:
        return True 
    else:
        return False
    
def is_token_expired(token):
    try:
        decoded = verify_decode_jwt(token)
        return False
    except jwt.ExpiredSignatureError:
        print("Your token has expired")
        return True
    
# testing user password database:
testingUsers = {
    'artist@groove.com': 'Artistlogin2023',
    'venue-manager@groove.com': 'Managerlogin2023'
    }

# testing utils ----

def create_test_gig(db):
    newArtist = Artist(name = 'Jordan',
                   email = 'artist@groove.com',
                   phone = '07563489658',
                   genres = ['disco', 'house'])
    newVenue = Venue(name="Tabac", 
                     genres=['disco', 'house'],
                     address="Mitchell Lane",
                     phone="01415721448",
                     image_link="https://shorturl.at/vL789")
            
    gig = Gig(venue_id = 1,
                   artist_id = 1,
                   time = '21:00',
                   hourly_rate = 5.5,
                   duration = 4.5,
                   is_booked = False)

    db.session.add(gig)
    db.session.add(newVenue)
    db.session.add(newArtist)
    db.session.commit()
    
def getUserAccessToken(userName):
    # client id and secret come from LogIn (Test Client)! which has password enabled under "Client > Advanced > Grant Types > Tick Password"
    url = f'https://{env.get("AUTH0_DOMAIN")}/oauth/token' 
    headers = {'content-type': 'application/json'}
    password = testingUsers[userName]
    parameter = { "client_id":env.get("AUTH0_CLIENT_ID"), 
                  "client_secret": env.get("AUTH0_CLIENT_SECRET"),
                  "audience": env.get("API_AUDIENCE"),
                  "grant_type": "password",
                  "username": userName,
                  "password": password, "scope": "openid" } 
    # do the equivalent of a CURL request from https://auth0.com/docs/quickstart/backend/python/02-using#obtaining-an-access-token-for-testing
    responseDICT = json.loads(requests.post(url, json=parameter, headers=headers).text)
    return responseDICT['access_token']

# memoize code from: https://stackoverflow.com/a/815160
# to avoid getting multiplce calls over many tests 
@memoize
def getUserTokenHeaders(userName):
    return { 'authorization': "Bearer " + getUserToken(userName)} 
  
