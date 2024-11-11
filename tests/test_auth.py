from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post('/auth/token', data={'username': user.username, 'password': user.clean_password})
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_token_expired_after_time(client, user):
    with freeze_time('2024-11-11 15:00:00'):
        response = client.post('/auth/token', data={'username': user.username, 'password': user.clean_password})
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-11-11 15:31:00'):
        response = client.put(
            f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}, json={'username': 'wrongwrong', 'email': 'wrong@wrong.com', 'password': 'wrong'}
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
