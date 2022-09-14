import pytest


@pytest.mark.django_db
def test_ad_create(client, user, category):
    data = {
        "name": "test name23",
        "author_id": user.pk,
        "price": 1000,
        "description": "test description",
        "is_published": False,
        "category_id": category.pk
    }
    expected_data = {
        "id": 1,
        "name": "test name23",
        "author_id": user.pk,
        "author": "user.name",
        "price": 1000,
        "description": "test description",
        "is_published": False,
        "category_id": category.pk,
        "image": None
    }
    response = client.post('/ad/create/', data, content_type="application/json")
    assert response.status_code == 200
    assert response.data == expected_data

