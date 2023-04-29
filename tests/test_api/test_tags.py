import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_get_tag_by_id(
    client: APIClient,
    tags_url: str,
    set_tags_to_db: None,
):
    response: Response = client.get(tags_url + "5/")
    assert response.status_code == status.HTTP_404_NOT_FOUND, (
        f"запрос по адресу `{tags_url + '5/'}` вернул некорректный "
        f"статус-код `{response.status_code}`"
    )

    response: Response = client.get(tags_url + "2/")
    assert response.status_code == status.HTTP_200_OK
    data: dict = response.json()
    assert data, "отсутсвует тег"
    assert data.keys() == {
        "id",
        "name",
        "color",
        "slug",
    }, "название полей тега не соотаетствует требуемым"


def test_get_list_tags(
    client: APIClient,
    tags_url: str,
    get_test_tags: dict,
    set_tags_to_db: None,
):
    response: Response = client.get(tags_url)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data, "в ответе нет тегов"

    data: list[dict[str, str]]
    tags = list(get_test_tags.values())
    tags.sort(key=lambda d: d["name"])
    data.sort(key=lambda d: d["name"])
    for i, resp_tag in enumerate(data):
        assert resp_tag.pop("id", None), "отсутсвует `id` тега"
        assert tags[i] == resp_tag, "данные тега не соответствуют ожидаемым"
