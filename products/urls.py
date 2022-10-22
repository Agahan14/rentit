from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PicturesViewSet,
    BannerViewSet,
    DateViewSet,
    DetailViewSet,
    DetailCategoryViewSet,
    ProductViewSet,
    ProductCategoryViewSet,
    CommentViewSet,
    FAQViewSet,
)

products_router = DefaultRouter()

products_router.register(r'pictures', PicturesViewSet)
products_router.register(r'banner', BannerViewSet)
products_router.register(r'dates', DateViewSet)
products_router.register(r'detail', DetailViewSet)
products_router.register(r'detail-category', DetailCategoryViewSet)
products_router.register(r'product', ProductViewSet)
products_router.register(r'product-category', ProductCategoryViewSet)
products_router.register(r'comment', CommentViewSet)
products_router.register(r'FAQ', FAQViewSet)

urlpatterns = [
    path('', include(products_router.urls))
]
