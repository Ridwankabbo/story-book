from django.db import models
PARTNERSHIP_TYPE_CHOICES = [
    ('educational', 'Educational Partner'),
    ('brand_collaborator', 'Brand Collaborator'),
    ('event/workshop', 'Event/Workshop Partner'),
    ('licensing', 'Licensing Partner'),
    ('sponsorship', 'Sponsorship Partner'),
    ('other', 'Other'),
]
class PartnershipInquary(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone=models.CharField(max_length=20,blank=True,null=True)
    company_name = models.CharField(max_length=255)
    partnership_type = models.CharField(max_length=255,choices=PARTNERSHIP_TYPE_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"{self.full_name} - {self.company_name} - {self.partnership_type}"
    
class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class ALHeraKitRequest(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    instution_name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    language_preference = models.CharField(max_length=100)
    classroom_kit=models.CharField(max_length=10)
    message= models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.full_name} - {self.email}"