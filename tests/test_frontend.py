import unittest
import pytest

from flask import abort, url_for
from flask_testing import TestCase

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.app_context():
        with app.test_client() as client:
            yield client

        
def test_base_route(client):
    rv = client.get('/')

    print(rv.get_data())
    assert rv.get_data() == b'Welcome to the SweepSouth API'
    assert rv.status_code == 200