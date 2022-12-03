from __future__ import absolute_import, unicode_literals
from users.models import User, GetTariff
from products.models import Product
from rentit.celery import app
from datetime import datetime
import pytz

utc=pytz.UTC


@app.task
def change_beat_status():
    tariff = GetTariff.objects.all()
    product = Product.objects.all()
    for i in tariff:

        if i.end_time <= datetime.now().replace(tzinfo=utc):
            i.user.is_business = False
            i.user.save()

    for products in product:

        if products.user.is_business == False:
            products.is_hot = False
            products.save()




