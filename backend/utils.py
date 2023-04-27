from backend.auth.auth import AuthError, requires_auth, verify_decode_jwt

def is_manager(token):
    decoded = verify_decode_jwt(token)
    permissions = decoded['permissions']
    if 'delete:gigs' in permissions:
        print("the current user is a manager")
        return True 
    else:
        return False
