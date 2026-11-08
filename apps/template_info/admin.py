from django import forms
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import PageContent, VehiclesCategory, VehiclesCategoryImage


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs']['multiple'] = True
        super().__init__(*args, **kwargs)


class MultiFileField(forms.FileField):
    widget = MultiFileInput

    def to_python(self, data):
        if not data:
            return []
        if not isinstance(data, (list, tuple)):
            data = [data]

        files = []
        for item in data:
            if item in (None, ''):
                continue
            value = super().to_python(item)
            if value:
                files.append(value)
        return files


class CategoryImageAdminForm(forms.ModelForm):
    image = MultiFileField(required=False)

    class Meta:
        model = VehiclesCategoryImage
        fields = '__all__'


class VehiclesCategoryImageInline(admin.TabularInline):
    model = VehiclesCategoryImage
    extra = 3
    fields = ('image', 'image_alt')


@admin.register(PageContent)
class PageContentAdmin(ModelAdmin):
    list_display = ('page_name', 'title', 'subtitle', 'updated_at')
    readonly_fields = ('updated_at',)


@admin.register(VehiclesCategory)
class VehiclesCategoryAdmin(ModelAdmin):
    inlines = [VehiclesCategoryImageInline]
    list_display = ('category', 'created_at', 'updated_at')
    search_fields = ('category',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(VehiclesCategoryImage)
class CategoryImageAdmin(ModelAdmin):
    form = CategoryImageAdminForm
    list_display = ('category', 'image_alt', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('category__category',)
