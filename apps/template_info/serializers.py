from rest_framework import serializers
from .models import PageContent, VehiclesCategoryImage


class PageContentSerializer(serializers.ModelSerializer):
    background_image = serializers.ImageField()

    class Meta:
        model = PageContent
        fields = ['page_name', 'title', 'subtitle', 'background_image', 'image_alt', 'updated_at']


class CategoryImageSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    image = serializers.ImageField()

    class Meta:
        model = VehiclesCategoryImage
        fields = ['category', 'category_name', 'image', 'image_alt', 'updated_at']

    def get_category_name(self, obj):
        return obj.get_category_display()
