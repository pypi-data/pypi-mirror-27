from flask import request
from flask_restplus import Resource

from inventorpy.client import Inventorpy
from inventorpy.http_api.restplus import api
from inventorpy.http_api.utils import get_database
from inventorpy.http_api.auth import token_required
from inventorpy.http_api.response import Response

user_namespace = api.namespace('user', description='Endpoint for all user functions')

@user_namespace.route('/')
class User(Resource):

    @api.response(201, 'Post was successful.')
    @token_required
    def post(self, user_email):
        posted_data = request.get_json()
        response = Inventorpy(get_database()
                              ).create_or_update(posted_data)
        if response.has_error:
            return Response(400, {"errors": response.errors})()
        return Response(201, {"user": response.data})()