from django.db import models

class Keyword(models.Model):
    name = models.CharField(blank=False, max_length=64)

