import sys
import os
from server import app
from ..config import client

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..'),
    ),
)


def test_full_booking_flow(client):
    """Test de toutes les fonctionnalités avec un club en manque de points"""

    login_page_response = client.get('/login')
    assert login_page_response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in login_page_response.data

    login_response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert login_response.status_code == 200
    assert b'Welcome' in login_response.data

    booking_page_response = client.get('/book/Fall Classic/Iron Temple')
    assert booking_page_response.status_code == 200
    assert b'Book' in booking_page_response.data

    booking_response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Fall Classic',
            'club': 'Iron Temple',
            'places': '2',
        },
    )
    assert booking_response.status_code == 200
    assert b'Great - booking complete!' in booking_response.data

    booking_response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Fall Classic',
            'club': 'Iron Temple',
            'places': '2',
        },
    )
    assert booking_response.status_code == 200
    assert b'Great - booking complete!' in booking_response.data

    booking_response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Fall Classic',
            'club': 'Iron Temple',
            'places': '2',
        },
    )
    assert booking_response.status_code == 200
    assert b'Insufficient points.' in booking_response.data

    summary_response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert summary_response.status_code == 200
    assert b'Welcome' in summary_response.data
    assert b'Iron Temple' in summary_response.data  # Confirm the correct club is shown
