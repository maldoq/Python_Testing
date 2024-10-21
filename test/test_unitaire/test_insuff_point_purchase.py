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


def test_purchase_places_insufficient_points(client):
    """Test de réservation de place avec un surplus de point"""
    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '6',
        },
    )
    assert response.status_code == 200
    assert 'Insufficient points.' in response.data.decode('utf-8')
