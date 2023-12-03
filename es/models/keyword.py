from django.db import models
from .article import Article

class Keyword(models.Model):
    key = models.TextField(blank=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

