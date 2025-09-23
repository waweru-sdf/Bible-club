import datetime
import jwt


SECRET_KEY = "super-secret-key"

def create_jwt(identity, expires_in=3600):
    """
    Create a JWT token with a given identity (e.g., user id).
    Default expiry is 1 hour.
    """
    payload = {
        "sub": identity,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in),
        "iat": datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_jwt(token):
    """
    Decode a JWT token. Raises jwt.ExpiredSignatureError or jwt.InvalidTokenError if invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
