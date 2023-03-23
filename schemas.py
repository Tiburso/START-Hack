from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from bip39_generator import generate_mnemonic_from_seed

from flask import Flask, request

# Create App and DB
app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

""" Domains ----------------------------------------------------------------- """

# Company owned wallets

class Wallet(db.Model):
    __tablename__ = "WALLETS"

    id   = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), unique=True, nullable=False)

    @property
    def mnemonic(self):
        return generate_mnemonic_from_seed(self.id)

# Games that are buyable by player users

class Game(db.Model):
    __tablename__ = "GAMES"

    id       = Column(Integer, primary_key=True, autoincrement=True)
    name     = Column(String(80), unique=True, nullable=False)
    cost     = Column(Integer, nullable=False)
    ipfsLink = Column(String(3000), nullable=False)

# Player Users that buy games

class User(db.Model):
    __tablename__ = "USERS"

    id       = Column(Integer, primary_key=True, autoincrement=True)
    name     = Column(String(80), unique=True, nullable=False)

class UserToGame(db.Model):
    __tablename__ = "USER_TO_GAME"

    userId = Column(Integer, ForeignKey("USERS.id"))
    gameId = Column(Integer, ForeignKey("GAMES.id"))

# Logs of all transactions

class Invoice(db.Model): pass

""" Routes ------------------------------------------------------------------ """

@app.route("/wallet/new", methods=["POST"])
def create_wallet():
    
    req = request.get_json()
    name = req["name"]

    wallet = Wallet(name=name)
    db.session.add(wallet)
    db.session.commit()

    return {"id": wallet.id, "mnemonic": wallet.mnemonic}, 200
    
@app.route("/user/new", methods=["POST"])
def create_user():
        
    req = request.get_json()
    name = req["name"]

    user = User(name=name)
    db.session.add(user)
    db.session.commit()

    return {"id": user.id}, 200

@app.route("/user/buyGame", methods=["POST"])
def buy_game(): # TODO - Add payment processing
            
    req = request.get_json()
    userId = req["userId"]
    gameId = req["gameId"]

    # TODO - Receive payment info and connect to BTCPay

    userToGame = UserToGame(userId=userId, gameId=gameId)
    db.session.add(userToGame)
    db.session.commit()

    return {"userId": userId, "gameId": gameId}, 200


if __name__ == "__main__":
    app.run(debug=True)