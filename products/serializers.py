from rest_framework import serializers

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
            'is_watched',
            'is_favorite',
            'created_date',
            'updated_date',
            'days',
            'rate',
            'category',
            'user',
        ]


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
