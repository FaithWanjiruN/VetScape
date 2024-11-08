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