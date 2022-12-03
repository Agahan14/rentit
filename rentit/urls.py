"""rentit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from products.urls import products_router
from orders.urls import orders_router
from users.urls import users_router
from patches import routers
from .yasg import urlpatterns as doc_url


router = routers.DefaultRouter()

router.extend(orders_router)
router.extend(users_router)
router.extend(products_router)


urlpatterns = [
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('accounts/', include('allauth.urls'), name='socialaccount_signup'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('products/', include(router.urls)),

]

urlpatterns += doc_url
