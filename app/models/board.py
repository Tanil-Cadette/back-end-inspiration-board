from app import db


class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    color = db.Column(db.Integer)
    cards = db.relationship("Card", back_populates="board")

    @db.validates("title", "owner")
    def no_empty_strings(self, key, value):
        value = str(value).strip()
        if not value:
            raise ValueError(f"{key} must be a non-empty string.")
        return value

    @db.validates("color")
    def color_24bit(self, key, value):
        if value is None:
            return value  # nullable=True
        value = int(value)
        if value < 0 or value > (256**3):
            raise ValueError(f"{key} must be a 24-bit integer.")
        return value

    def to_dict(self, color=False):
        board_dict = {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner,
        }
        if color:
            board_dict["color"] = self.color
        return board_dict

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

    def set_color(self, color):
        self.color = color
