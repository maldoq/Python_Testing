import sys
import os
import server

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..'),
    ),
)


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
