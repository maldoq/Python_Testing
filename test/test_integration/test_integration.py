import sys
import os
import json
import pytest
from server import app
from ..config import client

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..'),
    ),
)

# Path to your clubs.json file
JSON_FILE_PATH = 'C:/Users/Uriel-Marie/Documents/School/python/flaskdebug/python_testing1/Python_Testing/clubs.json'

# Fixture to handle setup and teardown


@pytest.fixture
def manage_clubs():
    # Step 1: Load original data
    with open(JSON_FILE_PATH, 'r') as f:
        original_data = json.load(f)

    # Make sure original_data["clubs"] is a list
    clubs_list = original_data.get("clubs", [])

    # Step 2: Add new clubs for testing
    new_clubs = [
        {"name": "Test Club 1", "email": "testclub1@example.com", "points": 23},
        {"name": "Test Club 2", "email": "testclub2@example.com", "points": 16},
    ]

    # Append new clubs to the original list of clubs
    updated_clubs_list = clubs_list + new_clubs
    original_data["clubs"] = updated_clubs_list

    # Write updated data to the file
    with open(JSON_FILE_PATH, 'w') as f:
        json.dump(original_data, f, indent=4)

    # Yield control to the test function
    yield

    # Step 3: Cleanup - Remove the added clubs and restore original data
    original_data["clubs"] = clubs_list  # Restore the original list of clubs
    with open(JSON_FILE_PATH, 'w') as f:
        json.dump(original_data, f, indent=4)


# Step 2: Test Club Registration
# Use the fixture to add and remove clubs during the test


def test_login(client, manage_clubs):
    # Perform the test for club registration
    """Test de la validation d'un email ajouté"""
    response = client.post(
        '/showSummary',
        data={'email': 'testclub1@example.com'},
    )
    assert response.status_code == 200
    assert "Welcome" in response.data.decode('utf-8')

    # Perform additional tests if needed
    # e.g., checking if Test Club 2 can be registered or if clubs are listed correctly
