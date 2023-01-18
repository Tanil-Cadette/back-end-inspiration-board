from app.models.card import Card
from app.models.board import Board
import pytest

# BOARD GET TESTS
def test_get_all_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_boards(client):
    pass

def test_get_one_board(client):
    pass

def test_get_all_cards_in_one_board(client):
    pass

def test_get_all_cards_in_one_board_with_no_cards(client):
    pass

# CARD TESTS

# CARD DELETE

def test_delete_one_card(client, create_one_card):
    #Act
    response = client.delete("/cards/1")
    response_body = response.get_json()
    #Assert
    assert response.status_code == 200
    assert "message" in response_body
    assert response_body == {
        "message": "Card 1 successfully deleted"
    }
    response = client.get("/cards/1")
    assert response.status_code == 404

def test_delete_one_card_when_there_are_no_cards(client):
    response = client.delete("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "message": "Id 1 not found"
    }
    assert Card.query.all() == []

# CARD PATCH

def test_patch_one_card_likes_count(client, create_card_with_likes):
    # Act
    response = client.patch("/cards/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body == {
        "board_id": None,
        "card_id": 1,
        "likes_count": 31,
        "message": "testing testing 123"
    }
    new_likes_card = Card.query.get(1)
    assert new_likes_card.likes_count == 31

# CARD GET

def test_get_one_card_by_id(client, create_one_card):
    #Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body == {
        "card": {
            "board_id": None,
            "card_id": 1,
            "likes_count": 0,
            "message": "testing testing 123"
        }
    }

def test_get_one_card_doesnt_exist(client):
    #Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "message": "Id 1 not found"
    }

# CARD POST 
def test_create_one_card_in_one_board(client, create_one_board):
    response = client.post("/cards", json={
        "message": "this is a test card",
        "board_id": 1
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "card" in response_body
    assert response_body == {
        "card": {
            "board_id": 1,
            "card_id": 1,
            "likes_count": 0,
            "message": "this is a test card"
        }
    }
    new_card = Card.query.get(1)
    assert new_card
    assert new_card.message == "this is a test card"
    assert new_card.likes_count == 0