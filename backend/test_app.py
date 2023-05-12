import json
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import unittest
from contextlib import contextmanager
from unittest.mock import MagicMock, patch
from dotenv import find_dotenv, load_dotenv

from flask import session, template_rendered, url_for, request
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from backend.models import Artist, Venue, Gig, db, db_drop_and_create_all, setup_db
from backend.utils import is_manager, is_token_expired, getUserAccessToken, create_test_gig


load_dotenv()
class GroovyTestCase(unittest.TestCase):
    """This class represents the Groovy test case"""


    def setUp(self):
        self.db = db
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "groovy_test"
        self.database_path = "postgresql://{}:@{}/{}".format('claudia','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db.app = self.app
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
 
    
    def login_as_manager(self, client):
        client.get('/login')
        token = getUserAccessToken('venue-manager@groove.com')
        return token

    def tearDown(self):
        """Executed after reach test"""
        db.session.remove()
        db.drop_all()
    

    def test_get_home_route_without_session_expect_pass(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to GROOVY", response.data)
        self.assertIn(b"Login", response.data)

    def test_get_home_route_expect_fail(self):
        response = self.client.post("/")
        self.assertEqual(response.status_code, 405)

 
    def test_get_home_route_with_valid_session_token_manager(self):
        with self.client as client:
            client.get('/login')
            token = getUserAccessToken('venue-manager@groove.com')
            session["user"] = token
            self.assertEqual(is_manager(token), True)
    
    def test_get_venues_route_when_not_logged_in_success(self):
        response = self.client.get('/venues')
        self.assertIn(b"You should be redirected automatically to target URL:", response.data)

    def test_get_venues_when_logged_in_success(self):
        with self.client as client:
            
            token = self.login_as_manager(client)
            # test that we've successfully logged in as a manager
            self.assertEqual(is_manager(token), True)
            with client.session_transaction() as session:
                session['user'] = {'access_token': token}
   
            venue = Venue(name="test venue", 
                     genres=['disco', 'house'],
                     address="Mitchell Lane",
                     phone="01415721448",
                     image_link="https://shorturl.at/vL789")
            
            db.session.add(venue)
            db.session.commit()

            response = client.get('/venues')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'test venue', response.data)

    def test_get_venues_when_logged_in_fail(self):
        with self.client as client:
            
            token = self.login_as_manager(client)
            # test that we've successfully logged in as a manager
            self.assertEqual(is_manager(token), True)
            with client.session_transaction() as session:
                session['user'] = {'access_token': token}
   
            venue = Venue(name="test venue", 
                     genres=['disco', 'house'],
                     address="Mitchell Lane",
                     phone="01415721448",
                     image_link="https://shorturl.at/vL789")
            db.session.add(venue)
            db.session.commit()
            response = client.post('/venues')
            self.assertEqual(response.status_code, 405)

    def test_get_artists_when_logged_out_success(self):
        response = self.client.get('/artists')
        self.assertIn(b"You should be redirected automatically to target URL:", response.data)
    
    def test_get_artists_when_logged_out_fail(self):
        response = self.client.post('/artists')
        self.assertEqual(response.status_code, 405)


    def test_get_artists_when_logged_in_success(self):
        with self.client as client:
            
            token = self.login_as_manager(client)
            # test that we've successfully logged in as a manager
            self.assertEqual(is_manager(token), True)
            with client.session_transaction() as session:
                session['user'] = {'access_token': token}
            artist = Artist(name = 'test artist',
                   email = 'artist@groove.com',
                   phone = '07563489658',
                   genres = ['disco', 'house'])
            db.session.add(artist)
            db.session.commit()
            response = client.get('/artists')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'test artist', response.data)
            
    
    def test_get_artists_when_logged_in_fail(self):
        with self.client as client:
            
            token = self.login_as_manager(client)
            # test that we've successfully logged in as a manager
            self.assertEqual(is_manager(token), True)
            with client.session_transaction() as session:
                session['user'] = {'access_token': token}
        response = self.client.post('/artists')
        self.assertEqual(response.status_code, 405)

    def test_get_gigs_when_logged_out_success(self):
        response = self.client.get('/gigs')
        self.assertIn(b"You should be redirected automatically to target URL:", response.data)
    
    def test_get_gigs_when_logged_out_fail(self):
        response = self.client.get('/gig')
        self.assertEqual(response.status_code, 404)

    def test_get_gigs_when_logged_in_as_manager_success(self):
        with self.client as client:
            token = self.login_as_manager(client)
            # test that we've successfully logged in as a manager
            self.assertEqual(is_manager(token), True)
            with client.session_transaction() as session:
                session['user'] = {'access_token': token}
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
            response = client.get('/gigs')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'4.5', response.data)
        
    def test_get_gigs_when_logged_in_as_manager_fail(self):
        with self.client as client:
            token = self.login_as_manager(client)
            # test that we've successfully logged in as a manager
            self.assertEqual(is_manager(token), True)
            with client.session_transaction() as session:
                session['user'] = {'access_token': token}
            response = client.get('/gig')
            self.assertEqual(response.status_code, 404)

    def test_post_gigs_success(self):
        with self.client as client:
            token = self.login_as_manager(client)
            response = client.post('/gigs', headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}'
                })
            
            self.assertIn(b'success', response.data)
            # Decode the response data from bytes to a string
            data = response.data.decode('utf-8')
            # Parse the response data as JSON
            data_dict = json.loads(data)
    
            # Check that the 'success' key exists in the dictionary
            self.assertIn('success', data_dict)
    
            # Check the value of the 'success' key
            self.assertEqual(data_dict['success'], True)
    
            # Check the response status code and headers
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

    def test_post_gigs_fail(self):
        with self.client as client:
            token = self.login_as_manager(client)
            response = client.post('/gig', headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}'
                })
        self.assertEqual(response.status_code, 404)

    def test_post_gigs_delete_success(self):
        with self.client as client:
            token = self.login_as_manager(client)
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
            response = client.post('/gigs/delete', headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}'
                },
                data='{"id": "1"}')
            
            data = response.data.decode('utf-8')
            # Parse the response data as JSON
            data_dict = json.loads(data)
            self.assertIn('message', data_dict)
            self.assertEqual(data_dict['message'], "Gig deleted")
            self.assertEqual(response.status_code, 200)

    def test_post_gigs_delete_fail(self):
         with self.client as client:
            token = self.login_as_manager(client)
            response = client.post('/gigs/delete', headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}'
                },
                data='{"id": "1"}')
            self.assertEqual(response.status_code, 404)

    def test_edit_get_gigs_success(self):
        with self.client as client:
            token = self.login_as_manager(client)
            # test that we've successfully logged in as a manager
            self.assertEqual(is_manager(token), True)
            with client.session_transaction() as session:
                session['user'] = {'access_token': token}
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
            response = client.get('/gigs/1/edit')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'4.5', response.data)
            self.assertIn(b'submit', response.data)
            self.assertIn(b'time', response.data)
            self.assertIn(b'Edit gig', response.data)
            self.assertIn(b'Edit gig', response.data)
            
    def test_edit_get_gigs_fail(self):
        with self.client as client:
            token = self.login_as_manager(client)
            response = client.get('/gigs/1/edit', headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}'
                })
            self.assertEqual(response.status_code, 404)


    def test_edit_post_gigs_success(self):
        with self.client as client:
            token = self.login_as_manager(client)
            create_test_gig()
            response = client.post('/gigs/1/edit', headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}'
                })
            self.assertEqual
        

    def test_edit_post_gigs_fail(self):
        pass

    def test_gigs_create_success(self):
        pass

    def test_gigs_create_fail(self):
        pass
            
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()