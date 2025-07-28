from dataclasses import asdict

from sqlalchemy import select

from fast_zero.models import User
from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username="alice",
            password="secret",
            email="teste@test",
        )

        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == "alice"))

    assert asdict(user) == {
        "id": 1,
        "username": "alice",
        "password": "secret",
        "email": "teste@test",
        "created_at": time,
    }
