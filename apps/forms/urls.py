from django.urls import path
from . import views

urlpatterns = [
    path('partnership-inquiry/', views.PartnershipInquaryAPIView.as_view(), name='partnership_inquiry'),
    path('newsletter-subscription/', views.NewsletterSubscriptionAPIView.as_view(), name='newsletter_subscription'),
    path('alhera-kit-request/', views.ALHeraKitRequestAPIView.as_view(), name='alhera_kit_request'),
]
