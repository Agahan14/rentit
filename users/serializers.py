from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import (
    User,
    Direction,
    Map,
    FollowingSystem,
    Tariff,
    Props,
    GetTariff,
)
from products.models import (
    Product,
    Rating,
)
from datetime import datetime, timedelta, date


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class RegisterUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    message = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "first_name",
            "email",
            # "phone",
            "password",
            "message",
        )

    def get_message(self, obj):
        return (
            "Verification message has been sent to your email, please verify your email"
        )

    # def validate_phone(self, value):
    #     if not value[1:].isnumeric():
    #         raise serializers.ValidationError('Phone must be numeric symbols')
    #     if value[:4] != '+996':
    #         raise serializers.ValidationError('Phone number should start with +996 ')
    #     elif len(value) != 13:
    #         raise serializers.ValidationError("Phone number must be 13 characters long")
    #     return value

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
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'birth_date',
            'age',
            'front_pictures',
            'back_pictures',
            'face_pictures',
            'email',
            'following',
            'followers',
            'follower_count',
            'following_count',
            'phone',
            'rate',
            'user_type',
            'is_business',
            'is_active',
            'is_staff',
            'is_superuser',
            'is_verified',
            'date_joined',
              ]

    def get_age(self, obj):
        today = date.today()
        if obj.birth_date is None:
            return None
        return today.year - obj.birth_date.year - (
                (today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))

    def get_follower_count(self, obj):

        return obj.followers.count()


    def get_following_count(self, obj):

        return obj.following.count()

        # total_rating =
    def get_rate(self, obj):
        user_id = obj.id
        ratings = Rating.objects.filter(product__user=user_id)
        total_rating = 0
        count = 0
        for i in ratings:
            total_rating += i.rating
            count += 1
        if total_rating != 0:
            return round(total_rating / count, 1)
        return total_rating


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'pictures',
            'passport_series',
            'passport_issues_date',
            'front_pictures',
            'back_pictures',
            'face_pictures',
            'email',
            'phone',
              ]


class UserMiniSerializer(serializers.ModelSerializer):
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
            'email',
            'phone',
            'is_staff',
            'is_superuser',
            'is_archive',
            'date_joined',
              ]
        read_only_fields = ['is_active']

    def get_age(self, obj):
        today = date.today()
        if obj.birth_date is None:
            return None
        return today.year - obj.birth_date.year - (
                (today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
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
            'address',
            'geolocation',
        ]


class UserContactSerializer(serializers.ModelSerializer):
    action = serializers.CharField()

    class Meta:
        model = FollowingSystem
        fields = [
            'user_to',
            'action',
        ]


class UserFollowingSerializer(serializers.ModelSerializer):
    following = UserListSerializer(many=True, read_only=True)
    followers = UserListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'following',
            'followers',
        ]


class ApproveUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'email',
            'front_pictures',
            'back_pictures',
            'face_pictures',
            'is_active',
        ]


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class ArchiveUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'email',
            'is_archive',
        ]


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = [
            'id',
            'name',
            'month',
            'price',
        ]


class GetTariffSerializer(serializers.ModelSerializer):
    # end_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = GetTariff
        fields = [
            'id',
            'user',
            'tariff',
            'pictures',
            'end_time',
            'is_approve',
        ]

    def update(self, instance, validated_data):
        user = validated_data.get('user')
        product = Product.objects.filter(user=user)
        instance.is_approve = validated_data.get('is_approve', instance.is_approve)
        instance.end_time = validated_data.get('end_time', instance.end_time)

        if instance.is_approve == True:
            user.is_business = True
            user.save()
            if product.exists():
                for i in product:
                    i.is_hot = True
                    i.save()

        instance.save()
        return instance


class PropsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Props
        fields = [
            'id',
            'name',
            'card_number',
        ]
