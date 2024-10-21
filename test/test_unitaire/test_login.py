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


def test_login_page(client):
    """Test de la connection de la page login"""
    response = client.get('/login')
    assert response.status_code == 200
    assert 'Welcome to the GUDLFT Registration Portal!' in response.data.decode('utf-8')
    assert 'Connection' in response.data.decode('utf-8')
