import pytest
from apistar import get_current_app, reverse_url, TestClient


app = get_current_app()
client = TestClient(app)


def register_request(first_name='Test', last_name='Tester', username='test', password='secret'):
    return client.post(reverse_url('authentication:register'), {
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'password': password,
    })


def login_request(username='test', password='secret'):
    return client.post(reverse_url('authentication:login'), {
        'username': username,
        'password': password,
    })


@pytest.mark.django_db(transaction=False)
def test_registration():
    # Royal path
    response = register_request()

    assert response.status_code == 200

    content = response.json()
    assert content.get('user', {}).get('username') == 'test'
    assert content.get('token') is not None

    # Invalid request data
    response = register_request()
    assert response.status_code == 400
    assert response.json().get('username').get('code') == 'user_exists'

    response = register_request(username=None)
    assert response.status_code == 400

    response = register_request(password=None)
    assert response.status_code == 400

    response = register_request(first_name=None)
    assert response.status_code == 400


@pytest.mark.django_db(transaction=False)
def test_login():
    # Royal path
    register_request()
    response = login_request()

    assert response.status_code == 200

    content = response.json()
    assert content.get('user', {}).get('username') == 'test'
    assert content.get('token') is not None

    # Invalid request data
    response = login_request(username=None)
    assert response.status_code == 400

    response = login_request(password=None)
    assert response.status_code == 400

    response = login_request(username='test', password='wrong')
    assert response.status_code == 401

    response = login_request(username='wrong', password='wrong')
    assert response.status_code == 401


@pytest.mark.django_db(transaction=False)
def test_authorization_header():
    token = register_request(username='testauth').json().get('token')

    # Define a dummy endpoint to test authentication
    from apistar import annotate, Include, Route
    from apistar.interfaces import Auth
    from apistar.http import Response
    from apistar.permissions import IsAuthenticated
    @annotate(permissions=[IsAuthenticated()])
    def dummy(auth: Auth):
        return Response(status=200, content='')

    # Small hack to add "dummy" endpoint during runtime
    prev_router_lookup = app.router.lookup
    app.router.lookup = lambda path, method: (dummy, {})

    response = client.get('/dummy', headers={'Authorization': 'Token {}'.format(token)})
    assert response.status_code == 200

    response = client.get('/dummy')
    assert response.status_code == 403

    response = client.get('/dummy', headers={'Authorization': 'Token {}'.format('wrongtoken')})
    assert response.status_code == 403

    # Return router to previous state
    app.router.lookup = prev_router_lookup
