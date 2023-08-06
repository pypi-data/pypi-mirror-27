from flask import request
from flask_restplus import Resource

from inventorpy.client import Inventorpy
from inventorpy.http_api.restplus import api
from inventorpy.http_api.utils import get_database
from inventorpy.http_api.auth import token_required
from inventorpy.http_api.response import Response


item_namespace = api.namespace('item', description='Endpoint for all items')
@item_namespace.route('/')
class Items(Resource):
    """Resource for items list
    """
    @token_required
    def get(self, user_email):
        query = {'entity_class': 'Item'}
        args = request.args
        for key in args:
            query[key] = args[key]

        inv_response = Inventorpy(get_database()).query(query)

        if inv_response.has_error:
            return Response(400, {"errors": inv_response.errors})()
        return Response(200, {"items": inv_response.data})()

    @api.response(201, 'Post was successful.')
    @token_required
    def post(self, user_email):
        data = request.get_json()
        inv_response = Inventorpy(get_database()
                              ).create_or_update(data)
        if inv_response.has_error:
            return Response(400, {"errors": inv_response.errors})()
        return Response(201, {"item": inv_response.data})()