# Populate all tables

from datetime import datetime, timedelta

from db.engine import session

from db.models.account import Account
from db.models.auth import Client, Token

import random


client = {
    "client_id": "TEST@AMER.OAUTHAP",
    "redirect_uri": "https://127.0.0.1:8080",
}

account = {
    "type": "MARGIN",
    "accountId": "111111111",
    "roundTrips": 0,
    "isDayTrader": False,
    "isClosingOnlyRestricted": False,
    "client_id": "TEST@AMER.OAUTHAP"
    }


def add_client():
    new_client = Client(**client)
    default_tokens = Token.generate_tokens()
    default_tokens["client_id"] = new_client.client_id
    new_tokens = Token(**default_tokens)
    session.add(new_client)
    session.add(new_tokens)
    session.commit()
    return new_client


def add_account():
    new_account = Account(**account)
    session.add(new_account)
    session.commit()
    return new_account


def add_all():
    add_client()
    add_account()
