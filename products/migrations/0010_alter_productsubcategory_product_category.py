# Generated by Django 3.2.2 on 2022-12-11 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_delete_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsubcategory',
            name='product_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_category', to='products.productcategory', verbose_name='Категория продукта'),
        ),
    ]
