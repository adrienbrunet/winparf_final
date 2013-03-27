from django.db import models
# from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Userwinparf(models.Model):
	''' Define the model of an userwinparf.'''
        user            = models.OneToOneField(User)
        name            = models.CharField(max_length=100)

        def __unicode__(self):
                return self.name