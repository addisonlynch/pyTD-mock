from .models import Token
from pyTD_mock.extensions.sqlalchemy import session
from .schemas import AuthTokenSchema

from flask import request
from flask_restful import (Resource, abort)


class AuthResource(Resource):

    @staticmethod
    def verify_tokens(token, client_id):
        """
        Verify that a client is associated with a given access token

        Parameters
        ----------
        token: str
            Access token string
        client_id: str
            Client ID

        Errors
        ------
        """
        # Get the client associated with the token
        token = session.query(Token)\
                       .filter_by(client_id=client_id).first()

        # Abort if no client associated with this token
        if not token:
            abort(401, message="Auth token not valid.")

        # Returns the full token record
        return token

    def post(self, *args, **kwargs):
        """
        Post refresh token to receive access token
        """
        # return request.form
        return request.form
        refresh_token = request.form['refresh_token']
        client_id = request.form['client_id']

        # Verify old tokens and remove them
        old_token = self.verify_tokens(refresh_token, client_id)
        session.delete(old_token)
        session.commit()

        # Add new tokens
        default_token = Token.generate_tokens()
        default_token["client_id"] = client_id
        new_token = Token(**default_token)
        session.add(new_token)
        session.commit()
        schema = AuthTokenSchema()
        return schema.dump(new_token)
