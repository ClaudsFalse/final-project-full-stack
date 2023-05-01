import os
import unittest
import json
import jwt
import time
import auth
from unittest.mock import patch, MagicMock
from flask_sqlalchemy import SQLAlchemy
from flask import template_rendered, session
from contextlib import contextmanager
from app import create_app
from backend.models import setup_db, Artist, Venue, db_drop_and_create_all, db
from backend.utils import is_manager, is_token_expired

class GroovyTestCase(unittest.TestCase):
    """This class represents the Groovy test case"""

    def setUp(self):
        print("start set up")
        self.db = db
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "groovy_test"
        self.database_path = "postgresql://{}:@{}/{}".format('claudia','localhost:5432', self.database_name)
        print(self.database_path)
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db.app = self.app
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        db.session.remove()
        db.drop_all()
    

    def test_get_home_route_without_session_expect_pass(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to GROOVY", response.data)
        self.assertIn(b"Login", response.data)

    def test_get_home_route_without_session_expect_fail(self):
        response = self.client.post("/")
        self.assertEqual(response.status_code, 405)

    @patch('auth.auth0.Auth0.authorize_access_token')
    @patch('auth.auth0.Auth0.get')
    def test_get_home_route_with_valid_session_token(self, mock_get, mock_auth):
        # Set token expiration time to past
        # Simulate a successful login
        mock_auth.return_value = {'access_token': 'my_token'}
        mock_get.return_value = {'email': 'test@groove.com'}

        # Send a login request to the server
        response = self.client.get('/login/callback?code=1234')

        # Check that the user was redirected to the gigs page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/gigs')
        
        # Check that the user's name was stored in the session
        with self.client.session_transaction() as session:
            self.assertIn('name', session)
            self.assertEqual(session['email'], 'test@groove.com')





            
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()