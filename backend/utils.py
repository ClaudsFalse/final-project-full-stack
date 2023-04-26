import os

def create_login_url():
    url = 'https://'
    url = url + os.environ['AUTH0_DOMAIN'] + '/authorize?audience='+ os.environ['API_AUDIENCE']+'&response_type=token&client_id='+ os.environ['CLIENT_ID'] + '&redirect_uri='+os.environ['AUTH0_URL']
    return url


