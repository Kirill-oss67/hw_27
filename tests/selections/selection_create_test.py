import pytest


@pytest.mark.django_db
def test_selection_create(client, user, ad, user_token):
    response = client.post('/selection/create/', {"name": "test selection", "owner": user.pk, "items": [ad.pk]},
                           content_type="application/json", HTTP_AUTHORIZATION="Bearer " + user_token)
    assert response.status_code == 201
    assert response.data == {"id": 1, "name": "test selection", "owner": user.pk, "items": [ad.pk]}
