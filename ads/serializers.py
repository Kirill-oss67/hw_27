from rest_framework import serializers

from ads.models import Location, User, Ad, Category, Selection


class UserCreateSerializer(serializers.ModelSerializer):
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
            obj, create = Location.objects.get_or_create(name=location)
            user.locations.add(obj)
        return user

    class Meta:
        model = User
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'role']
        model = User


class UserDetailSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field='name'
    )

    class Meta:
        exclude = ['password']
        model = User


class UserUpdateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        queryset=Location.objects.all(),
        many=True,
        slug_field='name'
    )

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop('locations')
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save(**kwargs)

        for location in self._locations:
            obj, create = Location.objects.get_or_create(name=location)
            user.locations.add(obj)
        return user

    class Meta:
        model = User
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        queryset=User.objects.all(),
        slug_field='username'
    )
    category = serializers.SlugRelatedField(
        required=False,
        queryset=Category.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Ad
        fields = "__all__"


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['items']
        model = Selection

class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdSerializer(many=True)
    class Meta:
        fields = '__all__'
        model = Selection

class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Selection
