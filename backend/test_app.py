import json
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import unittest
from contextlib import contextmanager
from unittest.mock import MagicMock, patch
from dotenv import find_dotenv, load_dotenv

from flask import session, template_rendered
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from backend.models import Artist, Venue, db, db_drop_and_create_all, setup_db
from backend.utils import is_manager, is_token_expired, getUserAccessToken, getUserTokenHeaders

load_dotenv()
class GroovyTestCase(unittest.TestCase):
    """This class represents the Groovy test case"""

    @contextmanager
    def captured_templates(app):
        recorded = []
        def record(sender, template, context, **extra):
            recorded.append((template, context))
        template_rendered.connect(record, app)
        try:
            yield recorded
        finally:
            template_rendered.disconnect(record, app)

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

    def tearDown(self):
        """Executed after reach test"""
        db.session.remove()
        db.drop_all()
    

    def test_get_home_route_without_session_expect_pass(self):
        response = self.client.get("/")
        print("--- Running test 1/3: test home route without user session")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to GROOVY", response.data)
        self.assertIn(b"Login", response.data)
        print("--- Test passed ✅")
      

    def test_get_home_route_without_session_expect_fail(self):
        print("--- Running test 2/3: test home route with wrong request")
        response = self.client.post("/")
        self.assertEqual(response.status_code, 405)
        print("--- Test passed ✅")

 
    def test_get_home_route_with_valid_session_token_manager(self):
        print("--- Running test 3/3: test /login route with a manager-role user")
        print("--- Expects user to be recognised as manager.")
        with self.client as client:
            client.get('/login')
            token = getUserAccessToken('venue-manager@groove.com')
            session["user"] = token
            self.assertEqual(is_manager(token), True)
            print("--- Test passed ✅")
            

## next: test routes for render template 




            
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()