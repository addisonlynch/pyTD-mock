from flask_restful import Api

from pyTD_mock.api.account.resources import AccountResource
from pyTD_mock.api.auth.resources import AuthResource

api = Api()

api.add_resource(AccountResource, '/v1/accounts/<account_id>',
                 endpoint='account')
api.add_resource(AuthResource, '/v1/oauth2/token')
