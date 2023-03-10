from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django_google_maps import fields as map_fields
from django.db import models
from django.utils import timezone
from orders.models import Cart
from rentit import settings


class SuperUser(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_verified", True)
        other_fields.setdefault("user_type", 'admin')

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True")
        if other_fields.get("is_active") is not True:
            raise ValueError("Superuser must be assigned to is_active=True")
        if other_fields.get("is_verified") is not True:
            raise ValueError("Superuser must be assigned to is_verified=True")
        if other_fields.get("user_type") != 'admin':
            raise ValueError("Superuser must be assigned to user_type=admin")
        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError("You must provide an email")

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        Cart.objects.create(user=user)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_type_choices = [
        ('client', 'client'),
        ('support', 'support'),
        ('admin', 'admin'),
    ]

    username = models.CharField(max_length=150, unique=True, null=True)
    email = models.EmailField(unique=True, null=True)
    pictures = models.ImageField(null=True, upload_to="images/")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=255, choices=user_type_choices,null=True, default='client')
    phone = models.CharField(max_length=255, unique=True, null=True)
    birth_date = models.DateField(null=True)
    following = models.ManyToManyField(
        'self',
        through='FollowingSystem',
        related_name='followers',
        symmetrical=False
    )
    front_pictures = models.ImageField(blank=True, null=True, upload_to='images/')
    back_pictures = models.ImageField(blank=True, null=True, upload_to='images/')
    face_pictures = models.ImageField(blank=True, null=True, upload_to='images/')
    passport_series = models.CharField(max_length=255, null=True, unique=True)
    passport_issues_date = models.DateField(auto_now_add=False, null=True, blank=True)
    is_archive = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_social = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'first_name']

    objects = SuperUser()

    def __str__(self):
        return f"{self.email}"


class PasswordReset(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)


class PasswordResetByPhone(models.Model):
    phone = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)


class Direction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    building_number = models.IntegerField(default=1)
    apartment_number = models.IntegerField(default=1)
    map = models.ForeignKey(
        "Map",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user


class Map(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)


class FollowingSystem(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created'),
        # unique_together = (('to_user', 'from_user'),)

    def __str__(self):
        return f'@{self.user_from.username} follows {self.user_to.username}'


class Props(models.Model):
    name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)


class Tariff(models.Model):
    name = models.CharField(max_length=255)
    month = models.IntegerField(default=1)
    price = models.FloatField(default=0)


class GetTariff(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.CASCADE,
        null=True,
    )
    is_approve = models.BooleanField(default=False)
    pictures = models.ImageField(blank=True, null=True, upload_to="images/")
    end_time = models.DateTimeField(auto_now_add=False, null=True)
