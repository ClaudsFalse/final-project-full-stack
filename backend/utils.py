import os

def create_login_url():
    url = 'https://'
    url = url + os.environ['AUTH0_DOMAIN'] + '/authorize?audience='+ os.environ['API_AUDIENCE']+'&response_type=token&client_id='+ os.environ['CLIENT_ID'] + '&redirect_uri='+'https://final-project-qnms.onrender.com/'
    return url





'''
https://fullstackclaud.eu.auth0.com/authorize?audience=final-project&response_type=token&client_id=hPqZKjCikVhCWNUeUjYcHj5yn00txS4J&redirect_uri=https://final-project-qnms.onrender.com

database_path = os.environ['DATABASE_URL']
'''