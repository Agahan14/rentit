from rest_framework import serializers
from collections import Counter
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
from users.models import User


class PicturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictures
        fields = [
            'id',
            'name',
            'image',
            'product',
            'banner',

        ]


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = [
            'id',
            'title',
            'description',
            'url',
            'image',
        ]


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = [
            'id',
            'name',
        ]


class DetailCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailCategory
        fields = [
            'id',
            'title',
            'detail',
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'product',
            'user',
            'replies',
            'creation_date',
        ]


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = [
            'id',
            'name',
            'sub_category',
            'detail_category',
        ]


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'detail',
            'price',
            'quantity',
            'views',
            'created_date',
            'updated_date',
            'days',
            'category',
            'user',
        ]

    def create(self, validated_data):
        user = validated_data.get('user')
        if Product.objects.filter(user=user).count() >= 10 and user.is_business == False:
            raise serializers.ValidationError('Sorry, but only business user can create more than 5 products.')
        elif Product.objects.filter(user=user).count() >= 50 and user.is_business:
            raise serializers.ValidationError('Sorry, but you can create only 50 products')
        return Product.objects.create(**validated_data)


class ProductDetailSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'detail',
            'price',
            'quantity',
            'rating',
            'views',
            'created_date',
            'updated_date',
            'days',
            'category',
            'user',
        ]

    def get_rating(self, obj):
        product_id = obj.id
        ratings = Rating.objects.filter(product=product_id)
        total_rating = 0
        count = 0
        for i in ratings:
            total_rating += i.rating
            count += 1
        if total_rating != 0:
            return round(total_rating / count, 1)
        return total_rating


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = [
            'id',
            'start_date',
            'end_date',
        ]


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
            'id',
            'question',
            'answer',
        ]


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = [
            'id',
            'product',
            'user',
            'rating',
        ]


class WishListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = WishList
        fields = [
            'id',
            'user',
            'product',
        ]
