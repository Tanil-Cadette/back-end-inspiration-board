from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)