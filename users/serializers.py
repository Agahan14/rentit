from rest_framework import serializers
from .models import (
    User,
    Address,
    Map,
)
from datetime import date


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class RegisterUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    birth_date = serializers.DateField(required=True)
    message = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "birth_date",
            "email",
            "phone",
            "password",
            "front_pictures",
            "back_pictures",
            "face_pictures",
            'message',
        )

    def get_message(self, obj):
        return (
            "Verification message has been sent to your email, please verify your email"
        )

    def validate_phone(self, value):
        if not value[1:].isnumeric():
            raise serializers.ValidationError('Phone must be numeric symbols')
        if value[:4] != '+996':
            raise serializers.ValidationError('Phone number should start with +996 ')
        elif len(value) != 13:
            raise serializers.ValidationError("Phone number must be 13 characters long")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ["token"]


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ["email", "password"]


class UserListSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'birth_date',
            'age',
            'is_active',
            'front_pictures',
            'back_pictures',
            'face_pictures',
            'email',
            'phone',
            'is_staff',
            'is_superuser',
            'date_joined',
              ]
        read_only_fields = ['is_active']

    def get_age(self, obj):
        today = date.today()
        if obj.birth_date is None:
            return None
        return today.year - obj.birth_date.year - (
                (today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id',
            'user',
            'country',
            'city',
            'district',
            'street',
            'postal_code',
            'building_number',
            'apartment_number',
            'map',
        ]


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = [
            'longitude',
            'latitude',
        ]
