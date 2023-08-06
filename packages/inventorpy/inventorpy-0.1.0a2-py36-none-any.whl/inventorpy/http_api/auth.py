from datetime import datetime, timedelta
from functools import wraps
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
from flask import request
from inventorpy.http_api.utils import is_testing
from inventorpy.http_api.response import Response

from inventorpy.http_api.config import SECRET_KEY


def decode_auth_token(auth_token, jwt_key=None):
    """
    Decotes the auth token
    :param auth_token:
    :return: integer or string
    """
    if not jwt_key:
        jwt_key = SECRET_KEY
    payload = jwt.decode(auth_token, jwt_key, algorithms='HS256')
    return payload


def encode_auth_token(user_email):
    """
    Generates the Auth Token
    :param user_uuid:
    :return: string
    """
    payload = {
        'exp': datetime.utcnow() + timedelta(days=0, hours=8),
        'iat': datetime.utcnow(),
        'user_email': user_email
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )


def token_required(f):
    """Authentication and authorization decorator
    Used to check authentication and permission
    based on the requests token included in an
    'Authentication' header and the user objects
    role.
    Then attaches a new token to the response"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Bypass wrapper if testing config == True
        if is_testing():
            user_email = 'testing'
            return f(user_email, *args, **kwargs)

        headers = dict(request.headers)

        try:
            token = headers['Authorization'].split()[1]
            payload = decode_auth_token(token)

        except (IndexError, KeyError):
            response = Response(
                code=401,
                results={"sent_headers": headers}
            )
            return response()

        except (DecodeError, ExpiredSignatureError) as e:
            response = Response(
                code=401,
                messages=[str(e)],
                results={"sent_headers": headers}
            )
            return response()

        # Run the wrapped function
        user_email = payload['user_email']
        response_data, code = f(user_email, *args, **kwargs)

        # update the response data with a new token
        new_token = encode_auth_token('some_subject').decode('utf8')
        response_data['auth_token'] = new_token

        return response_data, code

    return wrapper

{
    "code": 200,
    "results": {
        "user": {
            "uuid": "3993d196-9c9b-4238-9efa-8afda591211a",
            "entity_class": "User",
            "first_name": "admin",
            "last_name": "admin",
            "email": "admin@admin.com"
        }
    },
    "messages": [
        "Request fulfilled, document follows"
    ],
    "status": "success",
    "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MTM1ODIxNzgsImlhdCI6MTUxMzU1MzM3OCwidXNlcl9lbWFpbCI6ImFkbWluQGFkbWluLmNvbSJ9.nOaXToQ1gWSbr09bhvSPoAU8x9v6aNBH-bDM9PBZo9I"
}
