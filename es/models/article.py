from django.db import models

from .author import Author
from .keyword import Keyword
from .institution import Institution
from .refrence import Refrence

class Article(models.Model):
    title = models.CharField(blank=False, max_length=255)
    body = models.TextField(blank=False)
    resume = models.TextField(blank=False)
    url = models.CharField(blank=False, max_length=255)

    authors = models.ManyToManyField(Author)
    institutions = models.ManyToManyField(Institution)
    keywords = models.ManyToManyField(Keyword)
    refrences = models.ManyToManyField(Refrence)

    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
