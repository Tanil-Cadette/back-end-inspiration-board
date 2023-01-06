from app.models.card import Card
from app.models.board import Board
import pytest

# BOARD GET TESTS
def get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def get_one_board(client):
    pass

# CARD TESTS
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

def test_patch_one_card_likes_count(client, create_card_with_likes):
    response = client.patch("/cards/1")
    response_body = response.get_json()