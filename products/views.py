from django.shortcuts import get_object_or_404
from rest_framework.exceptions import (
    NotAcceptable,
    ValidationError,
    PermissionDenied,
)
from rest_framework.response import Response
from rest_framework import viewsets, status
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
    ProductDetailSerializer,
    RatingSerializer,
    WishListSerializer,
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
    Rating,
    WishList,
)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.views = obj.views + 1
        obj.save(update_fields=['views', ])
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=200)


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


class ProductDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        product = get_object_or_404(Product, pk=request.data["product"])
        rating = request.data['rating']
        if Rating.objects.filter(user=user, product=product).exists():
            raise ValidationError("You have already left your rating!")

        if user == product.user:
            raise PermissionDenied("This Is Your Product!")

        ratings = Rating(user=user, product=product, rating=rating)
        ratings.save()
        serializer = RatingSerializer(ratings)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WishListViewSet(viewsets.ModelViewSet):
    serializer_class = WishListSerializer
    queryset = WishList.objects.all()
    # lookup_field = 'user'

    def get_queryset(self):
        return WishList.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        product = get_object_or_404(Product, pk=request.data["product"])
        if WishList.objects.filter(user=user, product=product).exists():
            raise ValidationError("You have already added this product!")

        if user == product.user:
            raise PermissionDenied("This Is Your Product!")

        wishes = WishList(user=user, product=product)
        wishes.save()
        serializer = WishListSerializer(wishes)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FollowingViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Product.objects.all()
        following = self.request.user.following.all()

        return Product.objects.filter(user__in=following).order_by('created_date')
