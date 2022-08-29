from rest_framework import serializers

from ads.models import Location, User


class UserCreateSerializers(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        queryset=Location.objects.all(),
        many=True,
        slug_field='name'
    )
    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop('locations')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        for location in self._locations:
            obj , create = Location.objects.get_or_create(name=location)
            user.locations.add(obj)
        return user


    class Meta:
        model = User
        fields = '__all__'


