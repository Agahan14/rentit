from __future__ import absolute_import, unicode_literals
from users.models import User, GetTariff
from products.models import Product
from rentit.celery import app
from datetime import datetime
import pytz
from django.core.mail import send_mail
from rentit import settings

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

        if products.user.is_business is False:
            products.is_hot = False
            products.save()
            send_mail(
                subject='Rentit, your business account is expired!',
                message='If you want to renew your business account, please purchase!',
                from_email=getattr(settings, 'EMAIL_HOST_USER'),
                recipient_list=[products.user.email]
            )
