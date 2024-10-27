import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..'),
    ),
)


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
