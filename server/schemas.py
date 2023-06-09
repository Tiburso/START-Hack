from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from bip39_generator import generate_mnemonic_from_seed

from typing import Set

from app import db

""" Domains ----------------------------------------------------------------- """

# Games that are buyable by player users

class Game(db.Model):
    __tablename__ = "GAMES"

    id       = Column(Integer, primary_key=True, autoincrement=True)
    name     = Column(String(80), unique=True, nullable=False)
    forSale  = Column(Integer, nullable=False, default=1)
    cost     = Column(Integer, nullable=False)
    
    # turn this into a base64 encoded string
    ipfsLink = Column(String(64), nullable=False)
    
    # many-to-many relationship with users
    users: Mapped[Set["User"]] = relationship(secondary="USER_TO_GAME", back_populates="games")
    
# Player Users that buy games

class User(db.Model):
    __tablename__ = "USERS"

    id       = Column(Integer, primary_key=True, autoincrement=True)
    name     = Column(String(80), unique=True, nullable=False)
    address  = Column(String(80), unique=True, nullable=False) 
    
    # many-to-many relationship with games
    games: Mapped[Set["Game"]] = relationship(secondary="USER_TO_GAME", back_populates="users")

class UserToGame(db.Model):
    __tablename__ = "USER_TO_GAME"

    userId = Column(Integer, ForeignKey("USERS.id"), primary_key=True)
    gameId = Column(Integer, ForeignKey("GAMES.id"), primary_key=True)

# Logs of all transactions
