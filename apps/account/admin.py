from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from unfold.admin import ModelAdmin

# unregister groups
admin.site.unregister(Group)


from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin,ModelAdmin):
    list_display = (
        "email",
        "full_name",
        "date_joined",
        "is_active",
        "deleted_icon",   # 👈 delete indicator
    )

    search_fields = ("email", "full_name")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name", "dob", "profile_pic")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )

    def get_queryset(self, request):
        # ✅ show ALL users (including soft-deleted)
        return User.all_objects.all()

    # 🔥 DELETE INDICATOR ICON
    def deleted_icon(self, obj):
        if getattr(obj, "is_deleted", False):
            return format_html(
                '<span title="Soft deleted" style="color:red;font-size:18px;">🗑️</span>'
            )
        return format_html(
            '<span title="Active user" style="color:green;font-size:18px;">NO</span>'
        )

    deleted_icon.short_description = "Deleted"




# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'phone_number')
#     search_fields = ('user__email', 'user__first_name', 'user__last_name')
#     ordering = ('-user__date_joined',)
