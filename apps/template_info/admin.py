from django import forms
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import PageContent, VehiclesCategoryImage


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


@admin.register(PageContent)
class PageContentAdmin(ModelAdmin):
    list_display = ('page_name', 'title', 'subtitle', 'updated_at')
    readonly_fields = ('updated_at',)


@admin.register(VehiclesCategoryImage)
class CategoryImageAdmin(ModelAdmin):
    form = CategoryImageAdminForm
    list_display = ('category', 'image_alt', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('category',)

    def save_model(self, request, obj, form, change):
        files = request.FILES.getlist('image') or form.cleaned_data.get('image') or []
        if files:
            category = form.cleaned_data.get('category')
            image_alt = form.cleaned_data.get('image_alt', '')
            for file in files:
                VehiclesCategoryImage.objects.create(
                    category=category,
                    image=file,
                    image_alt=image_alt,
                )
            return

        super().save_model(request, obj, form, change)
