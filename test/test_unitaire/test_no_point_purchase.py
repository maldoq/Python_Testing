from datetime import datetime
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


def test_purchase_places_no_point(client):
    """Test de réservation de place avec un nombre de point nul"""
    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '0',
        },
    )
    assert response.status_code == 200
    assert 'You must book at least 1 place.' in response.data.decode('utf-8')
