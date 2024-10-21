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
