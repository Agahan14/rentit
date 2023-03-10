from rest_framework import serializers
import json
from .models import (
    Product,
    ProductCategory,
    Pictures,
    Banner,
    Comment,
    FAQ,
    Rating, ProductSubCategory, Brand,
)
from users.models import User


class PicturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictures
        fields = [
            'id',
            'image',
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


class ProductSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSubCategory
        fields = [
            'id',
            'name',
            'product_category',
            'characteristic',

        ]


class ProductCategorySerializer(serializers.ModelSerializer):
    sub_category = ProductSubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = ProductCategory
        fields = [
            'id',
            'name',
            'sub_category',
        ]


class UserProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'pictures',
        ]


class ProductSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    pictures = PicturesSerializer(many=True)
    user = UserProductSerializer(read_only=True, default=serializers.CurrentUserDefault())
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'user',
            'name',
            'description',
            'price',
            'currency',
            'views',
            'rating',
            'created_date',
            'updated_date',
            'sub_category',
            'user',
            'is_hot',
            'is_active',
            'characteristic',
            'likes',
            'pictures',
            'brand',
        ]
        read_only_fields = ('views', 'created_date', 'updated_date')

    def create(self, validated_data):
        pictures = validated_data.pop('pictures')
        product = Product.objects.create(**validated_data)
        for picture in pictures:
            Pictures.objects.create(**picture, product=product)
        return product

    def get_likes(self, obj):
        return obj.likes_count()

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

    def validate_user(self, user):
        count = Product.objects.filter(user=user).count()
        if count >= 15 and user.is_business is False:
            raise serializers.ValidationError('Sorry, but only business user can create more than 10 products.')
        elif count >= 50 and user.is_business:
            raise serializers.ValidationError('Sorry, but you can create only 50 products')
        return user

    def validate_pictures(self, pictures):
        if len(pictures) > 10:
            raise serializers.ValidationError('Sorry, but only business user can create more than 10 products.')
        return pictures


class ProductPostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    pictures = PicturesSerializer(many=True)
    # user = UserProductSerializer(read_only=True, default=serializers.CurrentUserDefault())
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'user',
            'name',
            'description',
            'price',
            'currency',
            'views',
            'rating',
            'created_date',
            'updated_date',
            'sub_category',
            'user',
            'is_hot',
            'is_active',
            'characteristic',
            'likes',
            'pictures',
            'brand',
        ]
        read_only_fields = ('views', 'created_date', 'updated_date')

    def create(self, validated_data):
        pictures = validated_data.pop('pictures')
        product = Product.objects.create(**validated_data)
        for picture in pictures:
            Pictures.objects.create(**picture, product=product)
        return product

    def get_likes(self, obj):
        return obj.likes_count()

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

    def validate_user(self, user):
        count = Product.objects.filter(user=user).count()
        if count >= 15 and user.is_business is False:
            raise serializers.ValidationError('Sorry, but only business user can create more than 10 products.')
        elif count >= 50 and user.is_business:
            raise serializers.ValidationError('Sorry, but you can create only 50 products')
        return user


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


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'sub_category']
