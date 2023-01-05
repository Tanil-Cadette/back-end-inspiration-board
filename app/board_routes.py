from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card


boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model


# ____________________________________________________________________________________________________________
# --------------------------------CREATE BOARD-----------------------------------------------------------------
# ____________________________________________________________________________________________________________
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    try:
        new_board = Board.from_dict(request_body)
    except KeyError:
        if "title" not in request_body or "owner" not in request_body:
            return make_response({"message": "invalid key"}, 400)

    new_board = Board.from_dict(request_body)

    db.session.add(new_board)
    db.session.commit()
    result = new_board.to_dict()

    return make_response(jsonify({"title": result}), 201)


# __________________________________________________________________________________________________________
# -----------------------------------GET BOARD---------------------------------------------------------------
# __________________________________________________________________________________________________________
@boards_bp.route("", methods=["GET"])
def get_boards():
    board_list = []
    id_query = request.args.get("board_id")

    if id_query:
        boards = Board.query.order_by(Board.board_id.asc()).all()
    else:
        boards = Board.query.all()

    for board in boards:
        board_list.append(board.to_dict())

    return jsonify(board_list), 200


@boards_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate_model(Board, board_id)
    board_dict = board.to_dict()

    return jsonify({"board": board_dict})


# __________________________________________________________________________________________________________
# --------------------------------UPDATE BOARD---------------------------------------------------------------
# __________________________________________________________________________________________________________
@boards_bp.route("/<board_id>", methods=["PUT"])
def update_board(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()

    board.update(request_body)
    board_dict = board.to_dict()
    db.session.commit()

    return make_response(jsonify({"board": board_dict}))


# ____________________________________________________________________________________________________________
# --------------------------------DELETE BOARD----------------------------------------------------------------
# ____________________________________________________________________________________________________________
@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_model(Board, board_id)
    board_dict = board.to_dict()

    db.session.delete(board)
    db.session.commit()

    return jsonify({"details": (f'Board {board_id} {board_dict["title"]} was deleted')})


# ____________________________________________________________________________________________________________
# --------------------------------CARD & BOARD----------------------------------------------------------------
# ____________________________________________________________________________________________________________
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_board_cards(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()

    cards_id = request_body["card_ids"]
    board.cards = []

    for id in cards_id:
        board.cards.append(Card.query.get(id))

    db.session.commit()
    response = {"board": board.board_id, "cards": cards_id}

    return jsonify(response), 200


@boards_bp.route("/<board_id>/cards", methods=["GET"])
def read_board_cards(board_id):
    board = validate_model(Board, board_id)
    cards_id = []

    for card in board.cards:
        card_dict = card.to_json()
        cards_id.append(card_dict)

    response_dict = board.to_dict()
    response_dict["cards"] = cards_id
    return jsonify(response_dict), 200
