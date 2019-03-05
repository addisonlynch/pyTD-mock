import time
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema


class AuthTokenSchema(ModelSchema):
    expires_in = fields.Method('get_access_expiry')
    refresh_token_expires_in = fields.Method('get_refresh_expiry')

    # Returns access expiration as ms since epoch
    def get_access_expiry(self, obj):
        return int(time.mktime(obj.access_expires.timetuple()))

    # Returns refresh expiration as ms since epoch
    def get_refresh_expiry(self, obj):
        return int(time.mktime(obj.refresh_expires.timetuple()))

    class Meta:
        fields = ('access_token', 'refresh_token', 'token_type', 'expires_in',
                  'refresh_token_expires_in', 'scope')
