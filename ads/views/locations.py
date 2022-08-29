from rest_framework.viewsets import ModelViewSet

from ads.models import Location
from ads.serializers import LocationSerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
