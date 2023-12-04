from django.db import models

class Institution(models.Model):
    name = models.CharField(blank=False, max_length=255)

