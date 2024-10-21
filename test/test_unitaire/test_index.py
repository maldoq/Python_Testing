import sys
import os
from server import app
import server
from ..config import client

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..'),
    ),
)


def test_index(client):
    """Test de la page d'accueil"""
    response = client.get('/')
    clubs = server.clubs
    assert response.status_code == 200
    assert 'Welcome to our website' in response.data.decode('utf-8')
    assert 'Here is the list of clubs' in response.data.decode('utf-8')
    for club in clubs:
        print(club['name'])
        assert club['name'] in response.data.decode('utf-8')
