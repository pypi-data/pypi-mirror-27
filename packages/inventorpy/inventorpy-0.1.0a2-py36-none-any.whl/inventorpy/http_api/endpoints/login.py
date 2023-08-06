from flask import request
from flask_restplus import Resource

from inventorpy.client import Inventorpy
from inventorpy.http_api.restplus import api
from inventorpy.http_api.utils import get_database
from inventorpy.http_api.auth import token_required, encode_auth_token
from inventorpy.http_api.response import Response

login_namespace = api.namespace('login', description='Endpoint for authenticating a user')

@login_namespace.route('/')
class Login(Resource):

    def post(self):
        # pull credentials from request
        auth = request.authorization
        if not auth:
            return Response(400)()

        # setup client with correct user
        inv = Inventorpy(get_database(), auth.username)

        if not inv.user:
            # user was not found
            return Response(401)()

        # confirm password
        if inv.user.check_password(auth.password):
            # build and return token response
            token = encode_auth_token(auth.username).decode()
            return Response(200, {"user": inv.user.to_dict()}, auth_token=token)()
        else:
            return Response(401)()

