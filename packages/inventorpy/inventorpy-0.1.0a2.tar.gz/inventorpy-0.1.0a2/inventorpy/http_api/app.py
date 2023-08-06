from flask import Blueprint, Flask
from flask_cors import CORS
import os

from inventorpy.http_api.restplus import api
from inventorpy.http_api.endpoints.dashboard import dashboard_namespace
from inventorpy.http_api.endpoints.users import user_namespace
from inventorpy.http_api.endpoints.items import item_namespace
from inventorpy.http_api.endpoints.login import login_namespace


def create_app(database):
    app = Flask(__name__)
    app.config['DATABASE'] = database
    app.config['SECRET_KEY'] = os.urandom(24)
    blueprint = Blueprint('api', __name__, url_prefix='/api')

    api.init_app(blueprint)
    api.add_namespace(login_namespace)
    api.add_namespace(item_namespace)
    api.add_namespace(user_namespace)
    api.add_namespace(dashboard_namespace)
    app.register_blueprint(blueprint)

    CORS(app)
    return app


def run_server():
    app = create_app()
    app.run(debug=True)


