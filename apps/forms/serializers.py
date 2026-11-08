from rest_framework import serializers
from .models import PartnershipInquary, NewsletterSubscription, ALHeraKitRequest

class PartnershipInquarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnershipInquary
        fields = '__all__'

class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = '__all__'

class ALHeraKitRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ALHeraKitRequest
        fields = '__all__'
