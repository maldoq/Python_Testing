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
    """Integrated test simulating the full flow from login to booking."""

    # Step 1: Load the login page
    login_page_response = client.get('/login')
    assert login_page_response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in login_page_response.data

    # Step 2: Submit login form with valid email
    login_response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert login_response.status_code == 200
    assert b'Welcome' in login_response.data  # Ensure the user is greeted after login

    # Step 3: Go to the booking page for a competition
    booking_page_response = client.get('/book/Spring Festival/Iron Temple')
    assert booking_page_response.status_code == 200
    assert b'Book' in booking_page_response.data  # Check if booking options are shown

    # Step 4: Submit a valid booking request
    booking_response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '2',
        },
    )
    assert booking_response.status_code == 200
    assert b'Great - booking complete!' in booking_response.data  # Confirm successful booking

    # Step 5: Check the club points after booking (mocked or from actual data)
    summary_response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert summary_response.status_code == 200
    assert b'Welcome' in summary_response.data
    assert b'Iron Temple' in summary_response.data  # Confirm the correct club is shown
    # Here, you might want to check if the points were reduced correctly
