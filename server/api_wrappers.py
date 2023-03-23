import requests
from flask import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from schemas import Wallet, User, Game, Invoice, UserToGame, db

STORE_ID = "Development"

def generate_invoice(amount: float, gameID: int, userID: int):
    """ Generates an invoice. """

    json = {
        "metadata": {
            "userId": gameID,
            "gameId": userID,
        },
        "receipt": {
            "enabled": True,
            "showQR": True,
            "showPayments": True
        },
        "amount": "1.00",
        "currency": "USD",
    }

    requests.post(f"https://localhost/api/v1/stores/{STORE_ID}/invoices", json=json)


def get_all_invoices():
    """ Gets all invoices. """

    response = requests.get(f"https://localhost/api/v1/stores/{STORE_ID}/invoices")
    return response.json()


# Webhook for when an invoice is settled
@app.route("???", methods=["POST"])
def invoice_settled():
    json = request.get_json()

    metadata = json["metadata"]
    userId = metadata["userId"]
    gameId = metadata["gameId"]

    userToGame = UserToGame(userId=userId, gameId=gameId)
    db.session.add(userToGame)
    db.session.commit()