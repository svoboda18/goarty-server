from django.db import models

class Author(models.Model):
    name = models.CharField(blank=False, max_length=255)
