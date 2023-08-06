from flask_restplus import Resource
from inventorpy.http_api.auth import token_required
from inventorpy.http_api.restplus import api
from inventorpy.http_api.utils import get_database
from inventorpy.http_api.response import Response
from inventorpy.client import Inventorpy


dashboard_namespace = api.namespace(
    'dashboard',
    description='Endpoint for dashboard stats'
)

@dashboard_namespace.route('/')
class Dashboard(Resource):

    @token_required
    def get(self, user_email):
        #client = Inventorpy(get_database(), user_email=user_email)
        return Response(200)()