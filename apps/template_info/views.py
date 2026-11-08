from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import PageContent, VehiclesCategoryImage
from .serializers import PageContentSerializer, CategoryImageSerializer


class PageContentDetailView(generics.RetrieveAPIView):
    queryset = PageContent.objects.all()
    serializer_class = PageContentSerializer
    lookup_field = 'page_name'
    permission_classes = [AllowAny]


class CategoryImageListAPIView(generics.ListAPIView):
    queryset = VehiclesCategoryImage.objects.select_related('category').all()
    serializer_class = CategoryImageSerializer
    permission_classes = [AllowAny]


class CategoryImageDetailAPIView(generics.ListAPIView):
    serializer_class = CategoryImageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_slug = self.kwargs.get('category')
        return VehiclesCategoryImage.objects.select_related('category').filter(
            category__category=category_slug
        ).order_by('-updated_at')
