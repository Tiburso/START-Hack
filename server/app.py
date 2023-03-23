from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

import requests
from base64 import urlsafe_b64encode, urlsafe_b64decode

URL = "http://localhost/api/v1"

# TODO: put this values into a .env file
API = "token bdbfa48fcab6f150b15b22c07c82ab2c11178425"
API_HEADER = { "Authorization": API }
STOREID = "Apg8Ceso5ZbUuZk7Kww6gkCZ4MJhGjgNveacGRiMCd9N"

configs = {
    "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:postgres@localhost:5432/postgres",
}

# Create App and DB
app = Flask(__name__)
CORS(app)
app.config.update(configs)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from base64 import urlsafe_b64encode, urlsafe_b64decode

# import models here for no circular imports
from schemas import Wallet, User, Game

""" Wallet Routes ----------------------------------------------------------- """

@app.route("/wallet/new", methods=["POST"])
def create_wallet():
    
    req = request.get_json()
    name = req["name"]

    wallet = Wallet(name=name)
    db.session.add(wallet)
    db.session.commit()

    return {"id": wallet.id, "mnemonic": wallet.mnemonic}, 200

@app.route("/wallet/<string:name>/get", methods=["GET"])
def get_wallet(name):
    wallet: Wallet = db.session.query(Wallet).filter_by(name=name).first()
    
    return {"id": wallet.id, "mnemonic": wallet.mnemonic}, 200

@app.route("/wallet/<string:name>/delete", methods=["DELETE"])
def delete_wallet(name):
    wallet: Wallet = db.session.query(Wallet).filter_by(name=name).first()
    db.session.delete(wallet)
    db.session.commit()

    return {"id": wallet.id}, 200

@app.route("/wallet/all", methods=["GET"])
def get_all_wallets():
    wallets: Wallet = db.session.query(Wallet).all()

    wallets = list(map(lambda wallet: {
        "id": wallet.id,
        "name": wallet.name,
        "mnemonic": wallet.mnemonic
    }, wallets))
        
    return {"wallets": wallets}, 200
    
""" Game Routes ------------------------------------------------------------- """    

@app.route("/game/new", methods=["POST"])
def create_game():
        
    req = request.get_json()
    name = req["name"]
    cost = req["cost"]
    ipfsLink: str = req["ipfsLink"]
    
    ipfsLink =  urlsafe_b64encode(ipfsLink.encode()).decode("utf-8")

    game = Game(name=name, cost=cost, ipfsLink=ipfsLink)
    db.session.add(game)
    db.session.commit()

    return {"id": game.id}, 200

@app.route("/game/<string:game>/delete", methods=["DELETE"])
def delete_game(game):
    game: Game = db.session.query(Game).filter_by(name=game).first()
    db.session.delete(game)
    db.session.commit()
    
    return {"id": game.id}, 200

@app.route("/game/all", methods=["GET"])
def get_all_games():
    games: Game = db.session.query(Game).all()
    
    games = list(map(lambda game: {
        "id": game.id,
        "name": game.name,
        "cost": game.cost,
        "ipfsLink": urlsafe_b64decode(game.ipfsLink.encode()).decode("utf-8")
    }, games))
    
    return {"games": games}, 200

@app.route("/game/<string:game>/get", methods=["GET"])
def get_game_users(game):
    game: Game = db.session.query(Game).filter_by(name=game).first()
    
    
    
    return jsonify(game), 200

""" User Routes -------------------------------------------------------------- """    
    
@app.route("/user/new", methods=["POST"])
def create_user():
        
    req = request.get_json()
    name = req["name"]

    user = User(name=name)
    db.session.add(user)
    db.session.commit()

    return {"id": user.id}, 200

@app.route("/user/<string:user>/delete", methods=["DELETE"])
def delete_user(user):
    user: User = db.session.query(User).filter_by(id=user).first()
    db.session.delete(user)
    db.session.commit()
    
    return {"id": user.id}, 200

@app.route("/user/<string:user>/buy/<string:game>", methods=["POST"])
def buy_game(user, game): # TODO - Add payment processing
    user: User = db.session.query(User).filter_by(id=user).first()
   
    # TODO - Receive payment info and connect to BTCPay
    body = {
        "metadata": {
            "user": user.name,
            "game-name": game["name"],
            "ipfsLink": game["ipfsLink"],
        },
        "checkout": {
            "speedPolicy": "HighSpeed",
            "defaultPaymentMethod": "BTC",
            "expirationMinutes": 90,
            "monitoringMinutes": 90,
            "paymentTolerance": 0,
            "redirectURL": "string", # probably mudar com frontend
            "redirectAutomatically": True,
            "requiresRefundEmail": True,
            "checkoutType": None,
        },
        "receipt": {
            "enabled": True,
            "showQR": True,
            "showPayments": True
        },
        "amount": game["cost"],
        "currency": "USD",
        "additionalSearchTerms": [ game["ipfsLink"] ]
    }
    
    r = requests.post(f'URL/stores/{STOREID}/invoices', json=body, headers=API_HEADER)
    # ver se precisamos mais alguma coisa desta resposta

    if r.status_code != 200:
        return Response(status=r.status_code) 

    return jsonify( r.json() ), 200

@app.route("/user/<string:user>/get", methods=["GET"])
def get_user_games(user):
    user: User = db.session.query(User).filter_by(id=user).first()

    user.games = list(map(lambda game: {
        "id": game.id,
        "name": game.name,
        "cost": game.cost,
        "ipfsLink": urlsafe_b64decode(game.ipfsLink.encode()).decode("utf-8")
    }, user.games))
    
    return jsonify(user), 200

""" Invoices Routes ---------------------------------------------------------- """

@app.route("/receive-payment", methods=["POST"])
def payment():
    req = request.get_json()
        
    meta = req["metadata"]  
    timestamp = req["timestamp"]
    
    pay = req["payment"]
    value = pay["value"]
    
    # add the game to the user 
    user: User = db.session.query(User).filter_by(name=meta["user"]).first()
    
    game: Game = db.session.query(Game).filter_by(meta["game-name"]).first()
    user.games.add(game)
    db.session.commit()
    
    # need to create a pull payment refering to 75% of the payment 
    ret_val = value * 0.75
    
    body = {
        "name": "Return fee",
        "description": "Value returned to vault wallet",
        "amount": ret_val,
        "currency": "BTC",
        "period": 604800, # check period 
        "BOLT11Expiration": None,
        "autoApproveClaims": True,
        "startsAt": timestamp,
        "expiresAt": timestamp + 60 * 5, # five minutes to deliver payment to main wallet
        "paymentMethods": 
        [
            "BTC"
        ]
    }
    
    res = requests.post(URL + f"/stores/{STOREID}/pull-payments", json=body, headers=API_HEADER)
    
    if res.status_code != 200:
        return Response(status=400)
    
    pullPaymentId = res.json()["id"]
    
    # finalize that pull payment with a payout
    body = {
        "destination": "VAULT_COIN_ADDRESS",
        "amount": ret_val,
        "paymentMethod": "BTC"
    }
    
    res = requests.post(URL + f"/pull-payments/{pullPaymentId}/payouts", json=body, headers=API_HEADER)
    
    return Response(status=res.status_code) 

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)