from app import db
from sqlalchemy.orm import validates


class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    cards = db.relationship("Card", back_populates="board")

    @validates("title", "owner")
    def no_empty_strings(self, key, value):
        value = str(value).strip()
        if not value:
            raise ValueError(f"{key} must be a non-empty string.")
        return value

    def to_dict(self):
        return {"board_id": self.board_id, "title": self.title, "owner": self.owner}

    @classmethod
    def filter_data(cls, board_data):
        accepted_data = ("title", "owner")
        return {field: board_data[field] for field in accepted_data}

    @classmethod
    def from_dict(cls, board_data):
        return Board(**Board.filter_data(board_data))

    def update(self, board_data):
        for field, value in Board.filter_data(board_data).items():
            setattr(self, field, value)
