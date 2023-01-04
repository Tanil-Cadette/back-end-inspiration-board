from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.card import Card
from app.models.board import Board

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")
boards_bp= Blueprint("boards", __name__, url_prefix="/boards")

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
# CREATE CARD
# ==================================
@cards_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()
    try:
        new_card= Card.create(request_body)
    except:
        if "message" not in request_body:
            return make_response({"details": "Invalid data"}, 400)
        
    new_card= Card.create(request_body)
    
    db.session.add(new_card)
    db.session.commit()
    card_dict= new_card.to_json()
    
    return make_response(jsonify({"card":card_dict}), 201)

# ==================================
# GET  CARD
# ==================================   
@cards_bp.route("", methods=["GET"]) 
def get_cards():
    cards_response= []
    cards= Card.query.all()
    
    for card in cards:
        cards_response.append(card.to_json())
    
    return jsonify(cards_response), 200

@cards_bp.route("/<card_id>", methods=["GET"]) 
def get_one_card(card_id):
    card= validate_id(Card, card_id)
    card_dict= card.to_json()
    
    return jsonify({'card':card_dict})
    
    
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
@cards_bp.route("<card_id>", methods=["PATCH"])
def edit_card_likes(card_id):
    card = validate_id(Card, card_id)

    card.likes_count += 1

    db.session.commit()

    return jsonify(card.to_json()), 200

