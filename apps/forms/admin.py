from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import *

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(ModelAdmin):
    list_display = ('email', 'subscribed_at')
    list_filter = ('subscribed_at',)

@admin.register(PartnershipInquary)
class PartnershipInquaryAdmin(ModelAdmin):
    list_display = ('full_name', 'email', 'company_name', 'created_at')
    list_filter = ('created_at',)

@admin.register(ALHeraKitRequest)
class ALHeraKitRequestAdmin(ModelAdmin):
    list_display = ('full_name', 'email', 'classroom_kit')
    list_filter = ('classroom_kit',)