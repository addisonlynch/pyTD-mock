from flask import request
from flask_restful import Resource, abort

from pyTD_mock.extensions.sqlalchemy import session
from pyTD_mock.api.auth.models import Client, Token

from .models import (Account, CurrentBalances, InitialBalances,
                     ProjectedBalances)
from .schemas import AccountSchema


class AccountResource(Resource):

    # @auth_check
    def get(self, account_id):

        access_token = request.headers.get("authorization")
        token_set = session.query(Token)\
                           .filter_by(access_token=access_token)\
                           .first()
        if not token_set:
            abort(401, message="Invalid auth token.")
        if not token_set.access_valid:
            return abort(401, message="Invalid auth token.")
        client_id = token_set.client_id
        client = session.query(Client)\
                        .filter_by(client_id=client_id)\
                        .first()
        if client.account.accountId != int(account_id):
            return abort(401, message="Not authorized.")
        accounts = session.query(Account)\
                          .filter(Account.accountId == account_id)\
                          .first()

        if not accounts:
            abort(404, message="Account %s doesn't exist." % account_id)
        schema = AccountSchema()
        dump = schema.dump(accounts)
        return {"securitiesAccount": dump}

    # @auth_check
    def post(self, account_id):
        json_data = request.get_json(force=True)

        # ensure account ID has been passed
        try:
            accountId = json_data["accountId"]
        except KeyError:
            abort(400, message="Invalid request. accountId must be provided.")

        # remove balances entries
        currentBalances = json_data.pop("currentBalances", None)
        initialBalances = json_data.pop("initialBalances", None)
        projectedBalances = json_data.pop("projectedBalances", None)

        # add account ID to balance objects
        if currentBalances:
            currentBalances["accountId"] = accountId
            c_model = CurrentBalances(**currentBalances)
            session.add(c_model)
        if initialBalances:
            initialBalances["accountId"] = accountId
            i_model = InitialBalances(**initialBalances)
            session.add(i_model)
        if projectedBalances:
            projectedBalances["accountId"] = accountId
            p_model = ProjectedBalances(**projectedBalances)
            session.add(p_model)

        account = Account(**json_data)

        session.add(account)
        session.commit()

        schema = AccountSchema()
        return schema.dumps(account)
