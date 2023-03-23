from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

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

from schemas import Wallet, User, Game, Invoice

""" Routes ------------------------------------------------------------------ """

""" Wallet Routes """

@app.route("/wallet/new", methods=["POST"])
def create_wallet():
    
    req = request.get_json()
    name = req["name"]

    wallet = Wallet(name=name)
    db.session.add(wallet)
    db.session.commit()

    return {"id": wallet.id, "mnemonic": wallet.mnemonic}, 200
    
""" Game Routes """    

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
    game: Game = db.session.query(Game).filter_by(id=game).first()
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

@app.route("/game/<string:game>/users", methods=["GET"])
def get_game_users(game):
    game: Game = db.session.query(Game).filter_by(id=game).first()
    users = list(game.users)
 
    return {"users": users}, 200
      
""" User Routes """    
    
@app.route("/user/new", methods=["POST"])
def create_user(g):
        
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
    # TODO - Receive payment info and connect to BTCPay
    game: Game = db.session.query(Game).filter_by(id=game).first()
    user: User = db.session.query(User).filter_by(id=user).first()
   
    user.games.add(game)
    db.session.commit()

    return {"userId": user, "gameId": game}, 200

@app.route("/user/<string:user>/games", methods=["GET"])
def get_user_games(user):
    user: User = db.session.query(User).filter_by(id=user).first()
    games = user.games
    
    games = list(map(lambda game: {
        "id": game.id,
        "name": game.name,
        "cost": game.cost,
        "ipfsLink": urlsafe_b64decode(game.ipfsLink.encode()).decode("utf-8")
    }, games))
    
    return {"games": games}, 200


if __name__ == "__main__":
    app.run(debug=True)