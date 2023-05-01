import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_get_ingredient_by_id(
    client: APIClient,
    ingridients_url: str,
    set_ingredientss_to_db: None,
):
    response: Response = client.get(ingridients_url + "5/")
    assert response.status_code == status.HTTP_404_NOT_FOUND, (
        f"запрос по адресу `{ingridients_url + '5/'}` вернул некорректный "
        f"статус-код `{response.status_code}`"
    )

    response: Response = client.get(ingridients_url + "2/")
    assert response.status_code == status.HTTP_200_OK
    data: dict = response.json()
    assert data, "отсутсвует тег"
    assert data.keys() == {
        "id",
        "name",
        "measurement_unit",
    }, "название полей тега не соотаетствует требуемым"


def test_get_list_ingredients(
    client: APIClient,
    ingridients_url: str,
    get_test_ingredients: dict,
    set_ingredientss_to_db: None,
):
    response: Response = client.get(ingridients_url)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data, "в ответе нет тегов"

    data: list[dict[str, str]]
    ingredients = list(get_test_ingredients.values())
    ingredients.sort(key=lambda d: d["name"])
    data.sort(key=lambda d: d["name"])
    for i, resp_ing in enumerate(data):
        assert resp_ing.pop("id", None), "отсутсвует `id` ингридиента"
        assert (
            ingredients[i] == resp_ing
        ), "данные ингридиента не соответствуют ожидаемым"
