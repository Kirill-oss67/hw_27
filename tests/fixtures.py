import pytest


@pytest.fixture
@pytest.mark.django_db
def user_token(client, django_user_model):
    username = "name"
    password = "12345"

    django_user_model.objects.create_user(username=username, password=password)

    response = client.post('/user/token/', {"username": username, "password": password},
                           content_type="application/json")
    return response.data['access']
