from django.contrib import admin
from django.urls import path, include

from chat.urls import chat_router
from products.urls import products_router
from orders.urls import orders_router
from products.views import ProductLikeView
from users.urls import users_router
from patches import routers
from .yasg import urlpatterns as doc_url


router = routers.DefaultRouter()

router.extend(orders_router)
router.extend(users_router)
router.extend(products_router)
router.extend(chat_router)


urlpatterns = [
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('accounts/', include('allauth.urls'), name='socialaccount_signup'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include(router.urls)),
    path('product-like/', ProductLikeView.as_view(), name='product-like'),
    path('chat/', include('chat.urls')),

]

urlpatterns += doc_url
