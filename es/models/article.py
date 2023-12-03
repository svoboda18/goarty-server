from django.db import models

class Article(models.Model):
    title = models.TextField(blank=False)
    body = models.TextField(blank=False)
    resume = models.TextField(blank=False)
    url = models.TextField(blank=False)
