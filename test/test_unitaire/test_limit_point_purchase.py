import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..'),
    ),
)


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
