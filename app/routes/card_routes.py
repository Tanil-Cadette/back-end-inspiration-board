from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.card import Card

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# ==================================
# Helper function to validate id
# ==================================
def validate_id(class_name,id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"Id {id} is an invalid id"}, 400))

    query_result = class_name.query.get(id)
    if not query_result:
        abort(make_response({"message":f"Id {id} not found"}, 404))

    return query_result


# ==================================
# DELETE one card by id
# ==================================
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    card = validate_id(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response({"message":f'Card {card.card_id} successfully deleted'}, 200)


# ==================================
# PATCH one card by id
# ==================================
@cards_bp.route("<card-id>", methods=["PATCH"])
def edit_card_likes(card_id):
    card = validate_id(Card, card_id)

    card.likes_count += 1

    db.session.commit()

    return jsonify(card.to_json()), 200
