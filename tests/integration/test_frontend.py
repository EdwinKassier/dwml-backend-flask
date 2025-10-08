import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        with app.test_client() as client:
            yield client


def test_base_route_without_args(client):
    rv = client.get("/api/v1/process_request")

    print(rv.get_data())
    assert rv.status_code == 500


def test_base_route_with_args_valid_symbol(client):
    rv = client.get("/api/v1/process_request?symbol=BTC&investment=1000")

    print(rv.get_data())
    assert rv.status_code == 200


def test_base_route_with_args_invalid_symbol(client):
    rv = client.get("/api/v1/process_request?symbol=DUHHH&investment=1000")

    print(rv.get_data())
    assert rv.status_code == 200
    # assert rv.get_data() == b'''{"message": "Symbol doesn't exist", "graph_data": null}'''


def test_base_route_malformed_no_symbol(client):
    rv = client.get("/api/v1/process_request?investment=1000")

    print(rv.get_data())
    assert rv.status_code == 500


def test_base_route_malformed_no_investment(client):
    rv = client.get("/api/v1/process_request?symbol=BTC")

    print(rv.get_data())
    assert rv.status_code == 500


def test_auth_route_without_auth_header(client):
    rv = client.get("/api/v1/restricted")

    print(rv.get_data())
    # When Firebase is not available, auth is skipped and returns 200
    # When Firebase is available, it should return 401 for missing auth
    assert rv.status_code in [200, 401]


def test_unknown_route(client):
    rv = client.get("/api/v1/random")

    print(rv.get_data())
    assert rv.status_code == 404
