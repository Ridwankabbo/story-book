from rest_framework import serializers
from .models import PageContent, VehiclesCategory, VehiclesCategoryImage


class PageContentSerializer(serializers.ModelSerializer):
    background_image = serializers.ImageField()

    class Meta:
        model = PageContent
        fields = ['page_name', 'title', 'subtitle', 'background_image', 'image_alt', 'updated_at']


class CategoryImageSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    image = serializers.ImageField()

    class Meta:
        model = VehiclesCategoryImage
        fields = ['id', 'category', 'category_name', 'image', 'image_alt', 'updated_at']

    def get_category(self, obj):
        return obj.category.category if obj.category else None

    def get_category_name(self, obj):
        return obj.category.get_category_display() if obj.category else None
