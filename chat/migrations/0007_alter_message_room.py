# Generated by Django 3.2.2 on 2022-12-17 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_remove_room_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to='chat.room'),
        ),
    ]
