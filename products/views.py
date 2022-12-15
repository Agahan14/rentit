from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    viewsets,
    status,
    filters, )
from rest_framework.exceptions import (
    ValidationError,
    PermissionDenied,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from users.pagination import CustomPagination
from .models import (
    Product,
    ProductCategory,
    Pictures,
    Banner,
    Comment,
    FAQ,
    Rating,
    ProductSubCategory,
    Brand,
)
from .serializers import (
    ProductSerializer,
    ProductCategorySerializer,
    PicturesSerializer,
    BannerSerializer,
    CommentSerializer,
    FAQSerializer,
    RatingSerializer,
    ProductSubCategorySerializer,
    BrandSerializer,
)


class MyProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = ('is_active',)

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filterset_fields = ['sub_category', 'sub_category__product_category']
    search_fields = ['name',]

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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class FAQViewSet(viewsets.ModelViewSet):
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()


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


class FollowingViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Product.objects.all()
        following = self.request.user.following.all()

        return Product.objects.filter(user__in=following).order_by('created_date')


class ProductSubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSubCategorySerializer
    queryset = ProductSubCategory.objects.all()


class ProductLikeView(APIView):
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product', '')
        if not product_id:
            return Response({'message': 'Incorrect data'}, status=400)
        if not self.request.user.is_anonymous:
            product = get_object_or_404(Product, id=product_id)
            if product.like.filter(id=self.request.user.id).exists():
                product.like.remove(request.user)
                return Response({'message': 'Disliked'}, status=200)
            else:
                product.like.add(request.user)
                return Response({'message': 'Liked'}, status=200)
        return Response({'message': 'User is not logged'})


class BrandViewSet(viewsets.ModelViewSet):
    model = Brand
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('sub_category',)
