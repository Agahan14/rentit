from django.db import models

from django.conf import settings

rates = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))


class Pictures(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/")
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    banner = models.ForeignKey(
        "Banner",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class Banner(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, blank=True)
    sub_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    detail_category = models.ForeignKey(
        "DetailCategory",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='detail_category'
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name="name", max_length=100)
    description = models.TextField(blank=True)
    detail = models.ForeignKey(
        "Detail",
        on_delete=models.CASCADE,
        related_name="information",
        blank=True,
        null=True,
    )
    price = models.FloatField(blank=True, null=True)
    is_watched = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(
        auto_now_add=False,
        blank=True,
        null=True,
    )
    quantity = models.IntegerField(default=1)
    days = models.ForeignKey("Date", on_delete=models.CASCADE, null=True)
    rate = models.PositiveSmallIntegerField(choices=rates, default=1)
    category = models.ForeignKey(
        ProductCategory,
        related_name="category",
        on_delete=models.CASCADE,
        null=True,
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Date(models.Model):
    start_date = models.DateField(auto_now_add=False)
    end_date = models.DateField(auto_now_add=False)

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"


class Detail(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DetailCategory(models.Model):
    title = models.CharField(max_length=255)
    detail = models.ManyToManyField(Detail, blank=True, null=True)

    def __str__(self):
        return self.title


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
