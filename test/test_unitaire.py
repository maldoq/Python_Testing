from datetime import datetime
import sys
import os
from server import app
import server
from .config import client

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


def test_login_page(client):
    """Test de la connection de la page login"""
    response = client.get('/login')
    assert response.status_code == 200
    assert 'Welcome to the GUDLFT Registration Portal!' in response.data.decode('utf-8')
    assert 'Connection' in response.data.decode('utf-8')


def test_show_summary_with_valid_email(client):
    """Test de la validation d'un vrai email"""
    response = client.post(
        '/showSummary',
        data={'email': 'admin@irontemple.com'},
    )
    competitions = server.competitions
    assert response.status_code == 200
    assert 'Welcome' in response.data.decode('utf-8')
    for competition in server.filter_upcoming_competitions(competitions):
        assert competition["name"] in response.data.decode('utf-8')


def test_show_right_competitions(client):
    """Test de l'affichage des competitions en date"""
    response = client.post(
        '/showSummary',
        data={'email': 'admin@irontemple.com'},
    )
    current_date = datetime.now()
    competitions = server.competitions
    for competition in competitions:
        if (
            competition["name"] in response.data.decode('utf-8')
            and datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S") <= current_date
        ):
            assert response.status_code == 404
        else:
            assert response.status_code == 200


def test_show_summary_with_invalid_email(client):
    """Test de la validation d'un faux email"""
    response = client.post(
        '/showSummary',
        data={'email': 'invalidemail@example.com'},
    )
    assert response.status_code == 200
    assert 'This email doesn&#39;t exist' in response.data.decode('utf-8')


def test_show_summary_with_no_email(client):
    """Test de la validation sans email"""
    response = client.post(
        '/showSummary',
        data={'email': ''},
    )
    assert response.status_code == 200
    assert "This email doesn&#39;t exist" in response.data.decode('utf-8')


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


def test_purchase_places_negative_point(client):
    """Test de réservation de place avec un nombre negatif de point"""
    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '-4',
        },
    )
    assert response.status_code == 200
    assert 'The value cannot be negative.' in response.data.decode('utf-8')


def test_purchase_places_limit_point(client):
    """Test de réservation de place avec le nombre limite de point qui est 12"""
    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '15',
        },
    )
    assert response.status_code == 200
    assert 'You can only book a maximum of 12 places per competition.' in response.data.decode('utf-8')
