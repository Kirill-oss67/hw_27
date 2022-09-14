import pytest

from ads.serializers import AdSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_list(client):
    ads_factories = AdFactory.create_batch(5)
    response = client.get('/ad/')
    assert response.status_code == 200
    assert response.data == {"count": 5, "next": None, "previous": None,
                             "results": AdSerializer(ads_factories, many=True).data}
