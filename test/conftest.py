from server import app
import pytest


@pytest.fixture
def client():
    app.testing = True  # Set the Flask app in testing mode
    with app.test_client() as client:  # Create a test client for Flask to simulate requests
        yield client  # Return the test client to be used in the tests
