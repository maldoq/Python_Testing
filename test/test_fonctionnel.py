import sys
import os
from server import app
from .config import client

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


def test_full_booking_flow_2(client):
    """Test de toutes les fonctionnalités avec une competition en manque de place"""

    login_page_response = client.get('/login')
    assert login_page_response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in login_page_response.data

    login_response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert login_response.status_code == 200
    assert b'Welcome' in login_response.data

    booking_page_response = client.get('/book/Fall Classic/Simply Lift')
    assert booking_page_response.status_code == 200
    assert b'Book' in booking_page_response.data

    booking_response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Fall Classic',
            'club': 'Simply Lift',
            'places': '5',
        },
    )
    assert booking_response.status_code == 200
    assert b'Great - booking complete!' in booking_response.data

    booking_response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Fall Classic',
            'club': 'Simply Lift',
            'places': '5',
        },
    )
    assert booking_response.status_code == 200
    assert b'Not enough places available.' in booking_response.data

    booking_response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '5',
        },
    )
    assert booking_response.status_code == 200
    assert b'Great - booking complete!' in booking_response.data

    summary_response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert summary_response.status_code == 200
    assert b'Welcome' in summary_response.data
    assert b'Iron Temple' in summary_response.data  # Confirm the correct club is shown
    # Here, you might want to check if the points were reduced correctly


def test_full_booking_flow_3(client):
    """Test de toutes les fonctionnalités avec un club voulant avoir plus de 12 places dans une competition"""

    login_page_response = client.get('/login')
    assert login_page_response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in login_page_response.data

    login_response = client.post('/showSummary', data={'email': 'kate@shelifts.co.uk'})
    assert login_response.status_code == 200
    assert b'Welcome' in login_response.data

    booking_page_response = client.get('/book/Spring Festival/She Lifts')
    assert booking_page_response.status_code == 200
    assert b'Book' in booking_page_response.data

    booking_response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'She Lifts',
            'places': '6',
        },
    )
    assert booking_response.status_code == 200
    assert b'Great - booking complete!' in booking_response.data

    booking_response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'She Lifts',
            'places': '7',
        },
    )
    assert booking_response.status_code == 200
    assert b'You can only book a maximum of 12 places per competition.' in booking_response.data

    summary_response = client.post('/showSummary', data={'email': 'kate@shelifts.co.uk'})
    assert summary_response.status_code == 200
    assert b'Welcome' in summary_response.data
    assert b'She Lifts' in summary_response.data  # Confirm the correct club is shown
    # Here, you might want to check if the points were reduced correctly
