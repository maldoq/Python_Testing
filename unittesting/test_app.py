import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch
from server import app, loadClubs, loadCompetitions 

# UNIT TESTS
@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test the index page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to our website' in response.data  
    assert b'Here is the list of clubs' in response.data

def test_index_page_shows_clubs(client):
    """Test that the index page displays the list of clubs."""
    
    # Mock data for clubs
    mock_clubs = [
        {'name': 'Club1', 'email': 'club1@example.com', 'points': 15},
        {'name': 'Club2', 'email': 'club2@example.com', 'points': 20}
    ]
    
    # Use patch to mock the loadClubs function
    with patch('server.loadClubs', return_value=mock_clubs) as mock_load:
        response = client.get('/')
        
        # Check the response status code
        assert response.status_code == 200
        
        # Ensure the mock was called
        assert mock_load.called
        
        # Verify that the club names and emails appear in the HTML response
        for club in mock_clubs:
            assert bytes(club['name'], 'utf-8') in response.data
            assert bytes(club['email'], 'utf-8') in response.data
            assert bytes(str(club['points']), 'utf-8') in response.data

def test_login_page(client):
    """Test the login page rendering."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data

# def test_login_post(client):
#     """Test submitting the login form with a valid email."""
    
#     # Prepare the data to be submitted
#     data = {'email': 'validemail@example.com'}
    
#     # Perform a POST request to the login route
#     response = client.post('/login', data=data)
    
#     # Check the response status code
#     assert response.status_code == 200
    
#     # Verify that the response contains the welcome message
#     assert b'Welcome, validemail@example.com!' in response.data


def test_show_summary_with_valid_email(client):
    """Test showSummary with a valid email."""
    response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_show_summary_with_invalid_email(client):
    """Test showSummary with an invalid email."""
    response = client.post('/showSummary', data={'email': 'invalidemail@example.com'})
    assert response.status_code == 200
    assert b"this mail doesn&#39;t exists" in response.data

def test_purchase_places_valid(client):
    """Test purchasing places with valid data."""
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '5'
    })
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data

def test_purchase_places_insufficient_points(client):
    """Test purchasing places with insufficient points."""
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': '11'
    })
    assert response.status_code == 200
    assert b"Your points ain&#39;t suficient" in response.data

# FUNCTIONAL TESTS
def test_functional_booking(client):
    """Simulate the entire booking process with functional tests."""
    # initial page
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data

    # Step 1: Login
    response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert response.status_code == 200
    assert b'Welcome' in response.data

    # Step 2: Book a competition
    response = client.get('/book/Spring Festival/Iron Temple')
    assert response.status_code == 200
    assert b'Book' in response.data

    # Step 3: Purchase places
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': '2'
    })
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data