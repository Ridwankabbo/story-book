from django.db import models


class PageContent(models.Model):
    PAGE_CHOICES = (
        ('hanger', 'Hanger'),
        ('vault', 'Vault'),
        ('community', 'Community'),
        ('clips', 'Clips'),
        ('home', 'Home'),
        ('the_story', 'The_story'),
        ('meet_the_guardians', 'Meet_the_guardians'),
        ('books_adventure', 'Books_adventure'),
    )

    page_name = models.CharField(
        max_length=50,
        choices=PAGE_CHOICES,
        unique=True,
        help_text="কোন পেজের data সেটা নির্ধারণ করে"
    )
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    background_image = models.ImageField(upload_to='page_backgrounds/')
    image_alt = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_page_name_display()} - {self.title}"


class VehiclesCategoryImage(models.Model):
    CATEGORY_CHOICES = (
        ('phantom_falcon', 'Phantom Falcon'),
        ('atlas_rover', 'Atlas Rover'),
        ('aqua_viper', 'Aqua Viper'),
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        help_text="Which category this image belongs to"
    )
    image = models.ImageField(upload_to='template_info/categories/', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category']
        verbose_name = 'Category Image'
        verbose_name_plural = 'Category Images'

    def __str__(self):
        return self.get_category_display()
