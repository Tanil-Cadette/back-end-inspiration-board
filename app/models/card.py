from app import db
from flask import abort, make_response

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, default=0)
    # color = db.Column(db.String)
    board_id= db.Column(db.Integer, db.ForeignKey('board.board_id'))
    board = db.relationship("Board", back_populates="cards")
    

    def to_json(self):
        card_dict= {}
        card_dict["card_id"]= self.card_id
        card_dict["message"]= self.message
        card_dict["likes_count"]= self.likes_count
        if self.board_id:
            card_dict["board_id"]= self.board_id
        
        return card_dict
    
    @classmethod
    def create(cls, request_body):
        new_card= Card(message=request_body["message"])
        
        return new_card
    