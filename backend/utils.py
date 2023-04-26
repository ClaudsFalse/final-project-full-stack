import os

def create_login_url():
    url = 'https://'
    url = url + os.environ['AUTH0_DOMAIN'] + '/authorize?audience='+ os.environ['API_AUDIENCE']+'&response_type=token&client_id='+ os.environ['CLIENT_ID'] + '&redirect_uri='+'https://final-project-qnms.onrender.com'
    return url





'''
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}

database_path = os.environ['DATABASE_URL']
'''