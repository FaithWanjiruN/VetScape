from django.apps import AppConfig
from django.db import models
from django.contrib.auth.models import User

class DjangoRegistrationTemplatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_registration_templates'

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.EmailField(default='default@example.com')

	def __str__(self):
		return self.user.username
	

class Clinic(models.Model):
    LOCATION_CHOICES = [
        ('Westlands', 'Westlands'),
        ('Kasarani', 'Kasarani'),
        ('Embakasi', 'Embakasi'),
        ('Langata', 'Langata')
    ]
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.location}"
