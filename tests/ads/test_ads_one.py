import pytest

from ads.serializers import AdSerializer


@pytest.mark.django_db
def test_ad_detail(client, ad, user_token):
    resp = client.get(f'/ad/{ad.id}/', content_type="application/json", HTTP_AUTHORIZATION="Bearer " + user_token)
    assert resp.status_code == 200
    assert resp.data == AdSerializer(ad).data
