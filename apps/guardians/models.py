from django.db import models
from apps.products.models import Product
# Create your models here.


class Country(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title


class CountryPhoto(models.Model):
    country = models.ForeignKey(
        Country,
        related_name="photos",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="countries/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Guardian(models.Model):
    name = models.CharField(max_length=100)
    age=models.IntegerField()
    about=models.TextField()
    description=models.TextField(blank=True,null=True)
    second_description=models.TextField(blank=True,null=True)
    nationality=models.CharField(max_length=50)
    roll_number=models.CharField(max_length=20, unique=True)
    personality=models.CharField(max_length=100)
    strengths=models.CharField(max_length=200)
    weaknesses=models.CharField(max_length=200)
    aspirational_angle=models.CharField(max_length=200)
    codename=models.CharField(max_length=50, unique=True)
    gadget=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class GuardianPhoto(models.Model):
    guardian = models.ForeignKey(
        Guardian,
        related_name="photos",
        on_delete=models.CASCADE,
    )
    profile_photo = models.ImageField(upload_to="guardians/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class GuardianQuestion(models.Model):
    guardian = models.ForeignKey(
        Guardian,
        related_name="questions",
        on_delete=models.CASCADE,
    )
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    


