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


def test_purchase_places_valid(client):
    """Test de réservation de place avec des données valides"""
    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '5',
        },
    )
    assert response.status_code == 200
    assert 'Great - booking complete!' in response.data.decode('utf-8')
