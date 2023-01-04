from app import db
from flask import abort, make_response

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    # likes_count = db.Column(db.Integer, default=0)
    # color = db.Column(db.String)
    # board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"))
    board_id= db.Column(db.Integer, db.ForeignKey('board.board_id'))
    board = db.relationship("Board", back_populates="cards")
    

    def to_json(self):
        card_dict= {}
        card_dict["card_id"]= self.card_id
        card_dict["message"]= self.message
        if self.board_id:
            card_dict["board_id"]= self.board_id
        
        return card_dict
            # return {
            #     "id": self.card_id,
            #     "message": self.message,
            #     "likes_count": self.likes_count,
            #     "color": self.color,
            #     "board_id": self.board_id
            # }
    
    def update_likes(self, request_body):
        try:
            self.likes_count = request_body["likes_count"]
        except KeyError as error:
            abort(make_response({'message': f"Missing attribute: {error}"}))
    
    @classmethod
    def create(cls, request_body):
        new_card= Card(message=request_body["message"])
        
        return new_card
    
        # new_card = cls(
        #     message = request_body["message"],
        #     color = request_body["color"],
        # )
        # return new_card