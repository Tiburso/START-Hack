from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from configs import VAULT_ADDRESS

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
migrate = Migrate(app, db, compare_type=True, render_as_batch=True)

from base64 import urlsafe_b64encode, urlsafe_b64decode

# import models here for no circular imports
from schemas import User, Game

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

@app.route("/game/<string:game>/get", methods=["GET"])
def get_game(game):
    game: Game = db.session.query(Game).filter_by(name=game).scalar()
    
    game = {
        "id": game.id,
        "name": game.name,
        "cost": game.cost,
        "address": game.address,
        "ipfsLink": urlsafe_b64decode(game.ipfsLink.encode()).decode("utf-8"),
        "users": list(map(lambda user: user.name, game.users))
    }

    return jsonify(game), 200

@app.route("/game/<string:game>/delete", methods=["DELETE"])
def delete_game(game):
    game: Game = db.session.query(Game).filter_by(name=game).scalar()
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
        "ipfsLink": urlsafe_b64decode(game.ipfsLink.encode()).decode("utf-8"),
        "users": list(map(lambda user: user.name, game.users))
    }, games))
    
    return {"games": games}, 200

""" User Routes -------------------------------------------------------------- """    
    
@app.route("/user/new", methods=["POST"])
def create_user():
        
    req = request.get_json()
    name = req["name"]
    address = req["address"]

    user = User(name=name, address=address)
    db.session.add(user)
    db.session.commit()

    return {"id": user.id}, 200

@app.route("/user/<string:user>/get", methods=["GET"])
def get_user(user):
    user: User = db.session.query(User).filter_by(name=user).scalar()

    user = {
        "id": user.id,
        "name": user.name,
        "address": user.address,
        "games": list(map(lambda game: {
            "id": game.id,
            "name": game.name,
            "cost": game.cost,
            "ipfsLink": urlsafe_b64decode(game.ipfsLink.encode()).decode("utf-8")
        }, user.games))
    }
    
    return jsonify(user), 200

@app.route("/user/<string:user>/delete", methods=["DELETE"])
def delete_user(user):
    user: User = db.session.query(User).filter_by(name=user).scalar()
    db.session.delete(user)
    db.session.commit()
    
    return {"id": user.id}, 200

@app.route("/user/all", methods=["GET"])
def get_users():
    users = db.session.query(User).all()
    
    users = list(map(lambda user: {
        "id": user.id,
        "name": user.name,
        "address": user.address,
        "games": list(map(lambda game: game.name, user.games))
    }, users))

    
    
    return jsonify(users), 200

@app.route("/user/<string:user>/buy/<string:game>", methods=["POST"])
def buy_game(user, game): # TODO - Add payment processing
    game: Game = db.session.query(Game).filter_by(name=game).scalar()
   
    body = {
        "metadata": {
            "user": user,
            "game-name": game.name,
            "from-user": ""
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
        "amount": game.cost,
        "currency": "USD",
        "additionalSearchTerms": [ game.ipfsLink ]
    }
    
    r = requests.post(f'{URL}/stores/{STOREID}/invoices', json=body, headers=API_HEADER)

    if r.status_code != 200:
        return Response(status=r.status_code) 

    return jsonify( r.json() ), 200

@app.route("/user/<string:user>/buy/<string:game>/other", methods=["POST"])
def buy_game_from_other(user, game):
    # Find one user that has the game for sale

    # Query the DB to find another user that has the game for sale
    other_user: User = db.session.query(User).filter(User.games.any(name=game)).first()

    body = {
        "metadata": {
            "user": user,
            "game-name": game,
            "from-user": other_user,
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
        "amount": game.cost,
        "currency": "USD",
        "additionalSearchTerms": [game.ipfsLink]
    }
    
    r = requests.post(f'{URL}/stores/{STOREID}/invoices', json=body, headers=API_HEADER)

    if r.status_code != 200:
        return Response(status=r.status_code) 

    return jsonify( r.json() ), 200
    
""" Invoices Routes ---------------------------------------------------------- """

@app.route("/finalize-game-purchase", methods=["POST"])
def finalize_game_purchase():
    req = request.get_json()
        
    meta = req["metadata"]  
    timestamp = req["timestamp"]
    
    pay = req["payment"]
    
    if pay is None:
        return Response(status=400)
    
    value = float(pay["value"])
    
    if "from-user" not in meta or  meta["from-user"] == "":
        # add the game to the user 
        user: User = db.session.query(User).filter_by(name=meta["user"]).scalar()
        game: Game = db.session.query(Game).filter_by(name=meta["game-name"]).scalar()
        user.games.add(game)
        db.session.commit()
        
        # need to create a pull payment refering to 75% of the payment 
        ret_val = value * 0.75
        
        body = {
            "name": "Return fee",
            "description": "Value returned to vault wallet",
            "amount": str(ret_val),
            "currency": "BTC",
            "period": 604800, # check period 
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
            print(res.content)
            return Response(status=res.status_code)
        
        pullPaymentId = res.json()["id"]
        
        # finalize that pull payment with a payout
        body = {
            "destination": VAULT_ADDRESS,
            "amount": ret_val,
            "paymentMethod": "BTC"
        }
        
        res = requests.post(URL + f"/pull-payments/{pullPaymentId}/payouts", json=body, headers=API_HEADER)
    
    else:
        # Add game to one user and remove from the other
        user: User = db.session.query(User).filter_by(name=meta["user"]).scalar()
        game: Game = db.session.query(Game).filter_by(meta["game-name"]).scalar()
        other_user: User = db.session.query(User).filter_by(name=meta["from-user"]).scalar()

        other_user.games.remove(game)
        user.games.add(game)

        db.session.commit()
        
        # need to create a pull payment refering to 75% of the payment 
        ret_val = value * 0.75
        
        body = {
            "name": "Return fee",
            "description": "Comissions returned to seller",
            "amount": ret_val,
            "currency": "BTC",
            "period": 604800, # check period 
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
            "destination": user.wallet,
            "amount": ret_val,
            "paymentMethod": "BTC"
        }
        
        res = requests.post(URL + f"/pull-payments/{pullPaymentId}/payouts", json=body, headers=API_HEADER)
    
    return Response(status=res.status_code) 

@app.route("/invoices/all", methods=["GET"])
def get_invoices():
    r = requests.get(f'{URL}/stores/{STOREID}/invoices', headers=API_HEADER)
    
    if r.status_code != 200:
        return Response(status=r.status_code)
    
    return jsonify( r.json() ), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)