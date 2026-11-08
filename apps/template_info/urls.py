from django.urls import path
from .views import PageContentDetailView, CategoryImageListAPIView, CategoryImageDetailAPIView

urlpatterns = [
    path('page-content/<str:page_name>/', PageContentDetailView.as_view(), name='page-content'),
    path('category-images/', CategoryImageListAPIView.as_view(), name='category-images-list'),
    path('category-images/<str:category>/', CategoryImageDetailAPIView.as_view(), name='category-images-detail'),
]