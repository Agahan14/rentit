# Generated by Django 3.2.2 on 2022-12-03 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_google_maps.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=150, null=True, unique=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('pictures', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(max_length=255)),
                ('user_type', models.CharField(choices=[('client', 'client'), ('support', 'support'), ('admin', 'admin')], default='client', max_length=255, null=True)),
                ('phone', models.CharField(max_length=255, null=True, unique=True)),
                ('birth_date', models.DateField(null=True)),
                ('front_pictures', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('back_pictures', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('face_pictures', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('passport_series', models.CharField(max_length=255, null=True, unique=True)),
                ('passport_issues_date', models.DateField(blank=True, null=True)),
                ('is_archive', models.BooleanField(default=False)),
                ('is_business', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_social', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', django_google_maps.fields.AddressField(max_length=200)),
                ('geolocation', django_google_maps.fields.GeoLocationField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetByPhone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Props',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('card_number', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('month', models.IntegerField(default=1)),
                ('price', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='GetTariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approve', models.BooleanField(default=False)),
                ('pictures', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('end_time', models.DateTimeField(null=True)),
                ('tariff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.tariff')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FollowingSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_from_set', to=settings.AUTH_USER_MODEL)),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_to_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=255)),
                ('building_number', models.IntegerField(default=1)),
                ('apartment_number', models.IntegerField(default=1)),
                ('map', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.map')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='users.FollowingSystem', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
