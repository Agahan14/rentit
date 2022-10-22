from rest_framework import viewsets
from .serializers import (
    ProductSerializer,
    ProductCategorySerializer,
    PicturesSerializer,
    BannerSerializer,
    DateSerializer,
    DetailSerializer,
    DetailCategorySerializer,
    CommentSerializer,
    FAQSerializer,
)
from .models import (
    Product,
    ProductCategory,
    Pictures,
    Banner,
    Date,
    Detail,
    DetailCategory,
    Comment,
    FAQ,
)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()


class PicturesViewSet(viewsets.ModelViewSet):
    serializer_class = PicturesSerializer
    queryset = Pictures.objects.all()


class BannerViewSet(viewsets.ModelViewSet):
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()


class DateViewSet(viewsets.ModelViewSet):
    serializer_class = DateSerializer
    queryset = Date.objects.all()


class DetailViewSet(viewsets.ModelViewSet):
    serializer_class = DetailSerializer
    queryset = Detail.objects.all()


class DetailCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = DetailCategorySerializer
    queryset = DetailCategory.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class FAQViewSet(viewsets.ModelViewSet):
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()
