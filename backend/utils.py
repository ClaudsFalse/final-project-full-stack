from os import environ as env
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

def create_login_url():
    url = 'https://'
    url = url + env['AUTH0_DOMAIN'] + '/authorize?audience='+ env['API_AUDIENCE']+'&response_type=token&client_id='+ env['CLIENT_ID'] + '&redirect_uri='+env['AUTH0_URL']
    return url


