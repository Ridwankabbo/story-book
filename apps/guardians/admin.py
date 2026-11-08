from django.contrib import admin
from .models import Guardian, GuardianPhoto, Country, CountryPhoto, GuardianQuestion
from unfold.admin import ModelAdmin, TabularInline


class GuardianPhotoInline(TabularInline):
    model = GuardianPhoto
    extra = 1


class CountryPhotoInline(TabularInline):
    model = CountryPhoto
    extra = 1


class GuardianQuestionInline(TabularInline):
    model = GuardianQuestion
    extra = 1

@admin.register(Guardian)
class GuardianAdmin(ModelAdmin):
    list_display = (
        "name",
        "country",
        "nationality",
        "age",
        "roll_number",
    )

    search_fields = ("name", "nationality", "age", "roll_number")
    ordering = ("-name",)
    inlines = [GuardianPhotoInline, GuardianQuestionInline]


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    list_display = (
        "title",
        "subtitle",
    )
    search_fields = ("title", "subtitle")
    ordering = ("title",)
    inlines = [CountryPhotoInline]


@admin.register(GuardianQuestion)
class GuardianQuestionAdmin(ModelAdmin):
    list_display = (
        "guardian",
        "question",
        "created_at",
    )
    search_fields = ("guardian__name", "question")
    ordering = ("-created_at",)

