from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Pictures(models.Model):
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='pictures',
    )


class Banner(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class ProductSubCategory(models.Model):
    name = models.CharField('Название подкатегории', max_length=256)
    product_category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        verbose_name='Категория продукта',
        related_name='sub_category')
    characteristic = ArrayField(models.CharField(
        max_length=256,
        blank=True,
        null=True),
        blank=True,
        null=True,
        verbose_name='Шаблон для характеристик',
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(verbose_name="Название производителя", max_length=256)
    sub_category = models.ManyToManyField(ProductSubCategory, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    currencies = [
        ('some', 'some'),
        ('dollar', 'dollar'),
    ]

    name = models.CharField(verbose_name="name", max_length=256)
    description = models.TextField(blank=True)
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.CASCADE)
    price = models.FloatField(blank=True, null=True)
    views = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True,
    )
    sub_category = models.ForeignKey(
        ProductSubCategory,
        related_name='product',
        on_delete=models.CASCADE,
        null=True,
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, related_name='product')
    is_hot = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    characteristic = models.JSONField('Характеристики продукта')
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='product_like', blank=True)
    currency = models.CharField(max_length=255, choices=currencies, default='som', null=True)

    def likes_count(self):
        return self.like.count()

    def __str__(self):
        return self.name


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    replies = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return f'{self.question}'


class Rating(models.Model):
    rates = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    rating = models.PositiveSmallIntegerField(choices=rates, default=1)



