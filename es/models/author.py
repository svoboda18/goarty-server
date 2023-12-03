from django.db import models
from .article import Article

class Author(models.Model):
    name = models.TextField(blank=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
