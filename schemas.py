from sqlalchemy import Column, Integer, String
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

class Wallet(db.Model):
    __tablename__ = "WALLETS"
    id   = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), unique=True, nullable=False)

    @property
    def mnemonic(self):
        return generate_mnemonic_from_seed(self.id)


class Game(db.Model):
    __tablename__ = "GAMES"
    id   = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), unique=True, nullable=False)
    cost = Column(Integer, nullable=False)


""" Routes ------------------------------------------------------------------ """

@app.route("/user/new", methods=["POST"])
def create_user():
    
    req = request.get_json()
    name = req["name"]

    wallet = Wallet(name=name)
    db.session.add(wallet)

    db.session.commit()

    return {"id": wallet.id, "mnemonic": wallet.mnemonic}, 200
    


if __name__ == "__main__":
    app.run(debug=True)