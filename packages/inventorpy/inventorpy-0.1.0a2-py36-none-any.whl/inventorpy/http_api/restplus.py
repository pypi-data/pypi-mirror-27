from flask_restplus import Api


api = Api(version='1.0', title='Inventorpy API',
          description='An API interface for interacting with Inventorpy',
          catch_all_404s=True)
