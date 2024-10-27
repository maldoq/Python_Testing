import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..'),
    ),
)


def test_show_summary_with_no_email(client):
    """Test de la validation sans email"""
    response = client.post(
        '/showSummary',
        data={'email': ''},
    )
    assert response.status_code == 200
    assert "This email doesn&#39;t exist" in response.data.decode('utf-8')
