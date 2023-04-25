import os
from flask import (
    Flask, 
    render_template, 
    request, 
    flash, 
    redirect, 
    url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/')
  def get_greeting():
    excited = os.environ['EXCITED']
    return render_template('frontend/index.html')

  return app

app = create_app()

if __name__ == '__main__':
    app.run()