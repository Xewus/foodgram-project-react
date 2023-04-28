from typing import Callable
import pytest
from rest_framework.test import APIClient

from rest_framework.response import Response


@pytest.fixture
def api_url() -> str:
    return "/api/"


@pytest.fixture
def users_url(api_url: str) -> str:
    return api_url + "users/"


@pytest.fixture
def token_url(api_url: str) -> str:
    return api_url + "auth/token/"


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def get_test_user_data() -> dict:
    return {
        "user_1": {
            "email": "Test_1@yandex.ru",
            "username": "TestUsernameOne",
            "first_name": "FirstNameOne",
            "last_name": "LastnameOne",
            "password": "Qwerty123",
        },
        "user_2": {
            "email": "Test_2@yandex.ru",
            "username": "TestUsernameTwo",
            "first_name": "FirstNameTwo",
            "last_name": "LastnameTwo",
            "password": "Qwerty123",
        },
    }


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**user_data):
        return django_user_model.objects.create_user(**user_data)

    return make_user


@pytest.fixture
def create_many_tests_users(db, django_user_model) -> Callable:
    def create_users(amount_users: int) -> None:
        [
            django_user_model.objects.create_user(
                email=f"email_{i}@gmail.com",
                username=f"username{i}",
                password=f"qaz123qazQ_{i}",
            )
            for i in range(amount_users)
        ]

    return create_users


@pytest.fixture
def login(
    client: APIClient,
    token_url: str,
    get_test_user_data: dict,
    create_user: Callable,
) -> tuple[APIClient, str, dict]:
    user: dict = get_test_user_data["user_1"]
    create_user(**user)
    login_data = {"email": user["email"], "password": user["password"]}
    response: Response = client.post(token_url + "login/", data=login_data)
    return client, response.json().get("auth_token"), user
