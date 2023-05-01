from typing import Callable

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

TOKEN = "Token "


def check_query_params(link: str, expect_params: set) -> None:
    # example page link:
    # http://foodgram.com/api/users/?page=2&limit=6
    query_params = link.split("?", 1)[1:]
    query_params = set(query_params[0].split("&")) if query_params else set()
    assert query_params == expect_params, (
        f"query-параметры в ссылке `{link.replace('http://testserver', '')}`"
        f" не соответствуют требуемым `{expect_params}`"
    )


class TestUsersListGet:
    def test_url(
        self,
        client: APIClient,
        users_url: str,
        create_many_tests_users: Callable,
    ):
        response: Response = client.get(users_url)
        assert response.status_code == status.HTTP_200_OK, (
            f"запрос по адресу `{users_url}` вернул некорректный "
            f"статус-код `{response.status_code}`"
        )
        data: dict = response.json()
        assert data["count"] == 0
        assert data["next"] is None
        assert data["previous"] is None
        assert data["results"] == []

    @pytest.mark.parametrize(
        "q_params, len_results, prev, next_, q_params_prev, q_params_next",
        [
            # 0 first page with default limit
            ("", 6, False, True, set(), {"page=2"}),
            # 1 first page with query-params
            ("?page=1&limit=1", 1, False, True, set(), {"page=2", "limit=1"}),
            # 2 second page with default limit
            ("?page=2", 6, True, True, set(), {"page=3"}),
            # 3 second page with query-params
            (
                "?page=2&limit=3",
                3,
                True,
                True,
                {"limit=3"},
                {"page=3", "limit=3"},
            ),
            # 4 last page with default limit
            ("?page=3", 2, True, False, {"page=2"}, set()),
            # 5 last page with  with query-params
            ("?page=3&limit=5", 4, True, False, {"page=2", "limit=5"}, set()),
        ],
    )
    def test_has_prev_next_page(
        self,
        client: APIClient,
        users_url: str,
        create_many_tests_users: Callable,
        q_params: str,
        len_results: int,
        prev: bool,
        next_: bool,
        q_params_prev: set,
        q_params_next: set,
    ):
        amount_users = 14
        create_many_tests_users(amount_users)
        url = users_url + q_params

        response: Response = client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            f"запрос по адресу `{url}` вернул некорректный "
            f"статус-код `{response.status_code}`"
        )

        data: dict = response.json()
        assert data["count"] == amount_users, (
            f"количество пользователей в поле `count` с адреса `{url}`"
            " не совпадает с количеством пользователей в базе"
        )
        assert len(data["results"]) == len_results, (
            "количество пользователей в поле `results`  с адреса "
            f"`{url}` не соответсвует запрошенному лимиту"
        )
        if prev:
            prev_page_link: str = data.get("previous")
            assert prev_page_link, "отсутствует ссылка на предыдущую страницу"
            check_query_params(prev_page_link, q_params_prev)
        else:
            assert (
                data["previous"] is None
            ), "первая страница не может иметь предыдущую"

        if next_:
            next_page_link: str = data.get("next")
            assert next_page_link, "отсутствует ссылка на следующую страницу"
            check_query_params(next_page_link, q_params_next)
        else:
            assert (
                data.get("next") is None
            ), "последняя страница не может иметь ссылку на следующую страницу"


class TestUsersListPost:
    @pytest.mark.parametrize(
        "reg_data, expect_data",
        [
            (
                {
                    "email": "test@gmail.com",
                    "username": "testuser",
                    "first_name": "testFirstName",
                    "last_name": "testLastName",
                    "password": "tStpss123wrD",
                },
                {
                    "id": 1,
                    "email": "test@gmail.com",
                    "username": "testuser",
                    "first_name": "testFirstName",
                    "last_name": "testLastName",
                },
            ),
            (
                {
                    "email": "test@gmail.com",
                    "username": "ТестовыйПользователь",
                    "first_name": "ТестовоеИмя",
                    "last_name": "ТестоваяФамилия",
                    "password": "tStpss123wrD",
                },
                {
                    "id": 1,
                    "email": "test@gmail.com",
                    "username": "ТестовыйПользователь",
                    "first_name": "ТестовоеИмя",
                    "last_name": "ТестоваяФамилия",
                },
            ),
        ],
    )
    def test_registration(
        self,
        client: APIClient,
        users_url: str,
        reg_data: dict,
        expect_data: dict,
    ):
        response: Response = client.post(users_url, reg_data)
        assert response.status_code == status.HTTP_201_CREATED, (
            f"запрос по адресу `{users_url}` вернул некорректный "
            f"статус-код `{response.status_code}`"
        )
        assert response.json() == expect_data, (
            "данные в ответе сервера после регистрации пользователя не "
            "соответствуют ожидаемым"
        )

    def test_correct_registration(
        self, client: APIClient, users_url: str, get_test_user_data: dict
    ):
        user_1: dict = get_test_user_data["user_1"]
        user_2: dict = get_test_user_data["user_2"]
        client.post(users_url, user_1)
        client.post(users_url, user_2)

        response: Response = client.get(users_url)
        assert response.status_code == status.HTTP_200_OK, (
            f"запрос по адресу `{users_url}` вернул некорректный "
            f"статус-код `{response.status_code}`"
        )
        data: dict = response.json()
        assert (
            len(data["results"]) == 2
        ), f"запрос на адрес `{users_url}` должен вернуть 2 пользователя"
        user_1.pop("password")
        user_2.pop("password")
        user_1.update({"id": 1, "is_subscribed": False})
        user_2.update({"id": 2, "is_subscribed": False})
        assert data["results"] == [
            user_1,
            user_2,
        ], "ответ сервера должен содержать данные всех пользователей"

    def test_repeat_data_for_registration(
        self, client: APIClient, users_url: str, get_test_user_data: dict
    ):
        user_1: dict = get_test_user_data["user_1"]
        user_repeat_email: dict = get_test_user_data["user_2"].copy()
        user_repeat_email["email"] = user_1["email"]
        user_repeat_username: dict = get_test_user_data["user_2"].copy()
        user_repeat_username["username"] = user_1["username"]

        client.post(users_url, user_1)

        response: Response = client.post(users_url, user_repeat_email)
        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
        ), "email должен быть уникальным"

        response: Response = client.post(users_url, user_repeat_username)
        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
        ), "username должен быть уникальным"

    @pytest.mark.parametrize(
        "reg_data, msg",
        [
            # 0 invalid email
            (
                {
                    "email": "testgmailcom",
                    "username": "testuser",
                    "first_name": "testFirstName",
                    "last_name": "testLastName",
                    "password": "tStpss123wrD",
                },
                "регистрация с некорректной почтой",
            ),
            # 1 invalid username, digit
            (
                {
                    "email": "test@gmail.com",
                    "username": "Тест0вый",
                    "first_name": "ТестовоеИмя",
                    "last_name": "ТестоваяФамилия",
                    "password": "tStpss123wrD",
                },
                "регистрация с некорректным юзернеймом",
            ),
            # 2 invalid username, sample eng+rus
            (
                {
                    "email": "test@gmail.com",
                    "username": "Тестqвый",
                    "first_name": "ТестовоеИмя",
                    "last_name": "ТестоваяФамилия",
                    "password": "tStpss123wrD",
                },
                "регистрация с некорректным юзернеймом",
            ),
            # 3 invalid first_name, digit
            (
                {
                    "email": "test@gmail.com",
                    "username": "testuser",
                    "first_name": "ТестовоеИмя11",
                    "last_name": "ТестоваяФамилия",
                    "password": "tStpss123wrD",
                },
                "регистрация с некорректным именем",
            ),
            # 4 invalid first_name, sample eng+rus
            (
                {
                    "email": "test@gmail.com",
                    "username": "testuser",
                    "first_name": "ТестовоеName",
                    "last_name": "ТестоваяФамилия",
                    "password": "tStpss123wrD",
                },
                "регистрация с некорректным именем",
            ),
            # 5 invalid last_name, digit
            (
                {
                    "email": "test@gmail.com",
                    "username": "testuser",
                    "first_name": "ТестовоеИмя",
                    "last_name": "ТестоваяФамилия11",
                    "password": "tStpss123wrD",
                },
                "регистрация с некорректной фамилией",
            ),
            # 6 invalid last_name, sample eng+rus
            (
                {
                    "email": "test@gmail.com",
                    "username": "testuser",
                    "first_name": "ТестовоеИмя",
                    "last_name": "ТестоваяSurname",
                    "password": "tStpss123wrD",
                },
                "регистрация с некорректной фамилией",
            ),
            # 7 no email
            (
                {
                    "username": "testuser",
                    "first_name": "testFirstName",
                    "last_name": "testLastName",
                    "password": "11edhjUFg",
                },
                "регистрация без почты",
            ),
            # 8 empty email
            (
                {
                    "email": "  ",
                    "username": "testuser",
                    "first_name": "testFirstName",
                    "last_name": "testLastName",
                    "password": "11ораККсс",
                },
                "регистрация без почты",
            ),
            # 9 no username
            (
                {
                    "email": "test@gmail.com",
                    "first_name": "testFirstName",
                    "last_name": "testLastName",
                    "password": "tStpss123wrD",
                },
                "регистрация без юзернейма",
            ),
            # 10 empty username
            (
                {
                    "email": "test@gmail.com",
                    "username": " ",
                    "first_name": "testFirstName",
                    "last_name": "testLastName",
                    "password": "11",
                },
                "регистрация без юзернейма",
            ),
            # 11 no first_name
            (
                {
                    "email": "test@gmail.com",
                    "username": "testuser",
                    "last_name": "testLastName",
                    "password": "tStpss123wrD",
                },
                "регистрация без имени",
            ),
            # 12 empty first_name
            (
                {
                    "email": "test@gmail.com",
                    "username": "testuser",
                    "first_name": "       ",
                    "last_name": "testLastName",
                    "password": "tStpss123wrD",
                },
                "регистрация без имени",
            ),
            # 13 no last_name
            (
                {
                    "email": "test@gmail.com",
                    "username": "testuser",
                    "first_name": "testFirstName",
                    "password": "tStpss123wrD",
                },
                "регистрация без фамилии",
            ),
            # 14 empty last_name
            (
                {
                    "email": "test@gmail.com",
                    "username": "testuser",
                    "first_name": "testFirstName",
                    "last_name": "    ",
                    "password": "tStpss123wrD",
                },
                "регистрация без фамилии",
            ),
            # 15 no password
            (
                {
                    "email": "test@gmail.com",
                    "username": "testuser",
                    "first_name": "testFirstName",
                    "last_name": "testLastName",
                },
                "регистрация без пароля",
            ),
            # 16 empty password
            (
                {
                    "email": "test@gmail.com",
                    "username": "testuser",
                    "first_name": "testFirstName",
                    "last_name": "testLastName",
                    "password": "            ",
                },
                "регистрация без пароля",
            ),
        ],
    )
    def test_invalid_data_for_registration(
        self, client: APIClient, users_url: str, reg_data: dict, msg: str
    ):
        response: Response = client.post(users_url, reg_data)
        if response.status_code == status.HTTP_201_CREATED:
            raise AssertionError(msg)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            f"запрос по адресу `{users_url}` вернул некорректный "
            f"статус-код `{response.status_code}`"
        )


class TestToken:
    @pytest.mark.parametrize(
        "pop_keys, invalid_data, msg",
        [
            # 0 without login data
            (("email", "password"), {}, "при отсутствии почты и пароля"),
            # 1 without email
            (("email",), {}, "при отсутствии почты"),
            # 2 not exists email
            (
                tuple(),
                {"email": "notexist@email.ru"},
                "для несуществующей почты",
            ),
            # 3 without password
            (("password",), {}, "при отсутствии пароля"),
            # 4 invalid password
            (tuple(), {"password": "invalid"}, "при неправильном пароле"),
        ],
    )
    def test_no_login(
        self,
        client: APIClient,
        token_url: str,
        create_user: Callable,
        get_test_user_data: dict,
        pop_keys: tuple,
        invalid_data: dict,
        msg: str,
    ):
        user = get_test_user_data["user_1"]
        create_user(**user)
        login_data = {"email": user["email"], "password": user["password"]}
        [login_data.pop(key, None) for key in pop_keys]
        login_data.update(invalid_data)

        response: Response = client.post(token_url + "login/", data=login_data)
        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
        ), f"токен выдан {msg}"

    def test_login(
        self,
        client: APIClient,
        token_url: str,
        create_user: Callable,
        get_test_user_data: dict,
    ):
        user = get_test_user_data["user_1"]
        create_user(**user)
        login_data = {"email": user["email"], "password": user["password"]}

        response: Response = client.post(token_url + "login/", data=login_data)
        assert response.status_code == status.HTTP_201_CREATED, (
            f"запрос по адресу `{token_url + 'login/'}` вернул некорректный "
            f"статус-код `{response.status_code}`"
        )
        data: dict = response.json()
        token = data.get("auth_token")
        assert token

    @pytest.mark.parametrize(
        "auth_header, msg",
        [
            # 0 no token
            ("", "доступ к %s без токена должен быть запрещён"),
            # 1 with invalid token
            (
                TOKEN + "dfshgdsrth" * 3,
                "доступ к %s с несществующим токеном должен быть запрещён",
            ),
        ],
    )
    def test_no_logout(
        self, client: APIClient, token_url: str, auth_header: str, msg: str
    ):
        url = token_url + "logout/"
        # with invalid token
        client.credentials(HTTP_AUTHORIZATION=auth_header)
        response: Response = client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, msg % url

    def test_logout(self, login: tuple[APIClient, str], token_url: str):
        client, token, _ = login
        url = token_url + "logout/"

        client.credentials(HTTP_AUTHORIZATION=TOKEN + token)
        response: Response = client.post(url)
        assert (
            response.status_code == status.HTTP_204_NO_CONTENT
        ), f"доступ к {url} с токеном должен быть разрешён"

        # token has been removed
        client.credentials(HTTP_AUTHORIZATION=TOKEN + token)
        response: Response = client.post(url)
        assert (
            response.status_code == status.HTTP_401_UNAUTHORIZED
        ), "токен не был удалён после логаута"


class TestUser:
    @pytest.mark.parametrize(
        "user_id, status_code",
        [
            # 0 not exists user
            (666, status.HTTP_404_NOT_FOUND),
            # 1 exists user
            (3, status.HTTP_200_OK),
        ],
    )
    def test_get_user_by_ID_for_anonim(
        self,
        client: APIClient,
        users_url: str,
        create_many_tests_users: Callable,
        user_id: int,
        status_code: int,
    ):
        create_many_tests_users(3)
        url = users_url + f"{user_id}/"

        response: Response = client.get(url)
        assert response.status_code == status_code, (
            f"запрос по адресу `{url}` вернул некорректный "
            f"статус-код `{response.status_code}`"
        )

    @pytest.mark.parametrize(
        "user_id, status_code, current_user",
        [
            # 0 not exists user
            (666, status.HTTP_404_NOT_FOUND, False),
            # 1 exists user
            (3, status.HTTP_200_OK, False),
            # 1 current user
            (1, status.HTTP_200_OK, True),
        ],
    )
    def test_get_user_by_ID_for_auth_user(
        self,
        users_url: str,
        login: tuple[APIClient, str, dict],
        create_many_tests_users: Callable,
        user_id: int,
        status_code: int,
        current_user: bool,
    ):
        url = users_url + f"{user_id}/"
        client, token, user_data = login
        create_many_tests_users(3)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response: Response = client.get(url)
        assert response.status_code == status_code, (
            f"запрос по адресу `{url}` вернул некорректный "
            f"статус-код `{response.status_code}`"
        )

        if current_user:
            assert response.json()["email"] == user_data["email"]

    @pytest.mark.parametrize(
        "auth_header, statuse_code, msg",
        [
            # 0 without token
            (
                "",
                status.HTTP_401_UNAUTHORIZED,
                "доступ к %s без токена должен быть запрещён",
            ),
            # 1 invalid token
            (
                TOKEN + "dfshgdsrth" * 3,
                status.HTTP_401_UNAUTHORIZED,
                "доступ к %s с несществующим токеном должен быть запрещён",
            ),
        ],
    )
    def test_me_for_anonim(
        self,
        client: APIClient,
        users_url: str,
        auth_header: str,
        statuse_code: int,
        msg: str,
    ):
        url = users_url + "me/"
        client.credentials(HTTP_AUTHORIZATION=auth_header)
        response: Response = client.get(url)
        assert response.status_code == statuse_code, msg % url

    def test_me(
        self,
        login: tuple[APIClient, str],
        users_url: str,
        create_many_tests_users: Callable,
    ):
        client, token, user_data = login
        create_many_tests_users(3)
        url = users_url + "me/"
        client.credentials(HTTP_AUTHORIZATION=TOKEN + token)
        response: Response = client.get(url)
        assert (
            response.status_code == status.HTTP_200_OK
        ), f"доступ к {url} с токеном должен быть разрешён"

        data: dict = response.json()
        assert data["username"] == user_data["username"].capitalize(), (
            "Во избежание подделки юзернеймов и обеспечение их уникальности "
            "следует привести юзернеймы к единому формату"
        )
        assert data["email"] == user_data["email"]
        assert data["first_name"] == user_data["first_name"]
        assert data["last_name"] == user_data["last_name"]
        assert data["is_subscribed"] is False

    @pytest.mark.parametrize(
        "auth_header, statuse_code, msg",
        [
            # 0 without token
            (
                "",
                status.HTTP_401_UNAUTHORIZED,
                "доступ к %s без токена должен быть запрещён",
            ),
            # 1 invalid token
            (
                TOKEN + "dfshgdsrth" * 3,
                status.HTTP_401_UNAUTHORIZED,
                "доступ к %s с несществующим токеном должен быть запрещён",
            ),
        ],
    )
    def test_change_password_for_anonim(
        self,
        client: APIClient,
        users_url: str,
        auth_header: str,
        statuse_code: int,
        msg: str,
    ):
        url = users_url + "set_password/"
        data = {
            "new_password": "New443Pass",
            "current_password": "password",
        }
        client.credentials(HTTP_AUTHORIZATION=auth_header)
        response: Response = client.post(url, data)
        assert response.status_code == statuse_code, msg % url

    def test_change_password(
        self, login: tuple[APIClient, str], users_url: str, token_url: str
    ):
        client, token, user_data = login
        url = users_url + "set_password/"

        login_data = {
            "email": user_data["email"],
            "password": user_data["password"],
        }
        data = {
            "new_password": "New443Pass",
            "current_password": user_data["password"] + "tr",
        }

        # no data
        client.credentials(HTTP_AUTHORIZATION=TOKEN + token)
        response: Response = client.post(url)
        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
        ), "при изменении пароля следует передать новые данные"

        # invalid data
        client.credentials(HTTP_AUTHORIZATION=TOKEN + token)
        response: Response = client.post(url)
        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
        ), "нельзя измененить пароль не зная старого"

        # correct
        data["current_password"] = user_data["password"]
        client.credentials(HTTP_AUTHORIZATION=TOKEN + token)
        response: Response = client.post(url, data)
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            f"запрос по адресу `{url}` вернул некорректный "
            f"статус-код `{response.status_code}`"
        )

        client.post(token_url + "logout/")
        response: Response = client.post(token_url + "login/", data=login_data)
        assert (
            response.status_code == status.HTTP_401_UNAUTHORIZED
        ), "нельзя совершить вход со старым паролем"
