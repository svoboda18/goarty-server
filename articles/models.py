from django.db import models

class Author(models.Model):
    name = models.CharField(blank=False, max_length=255)

class Institution(models.Model):
    name = models.CharField(blank=False, max_length=255)

class Keyword(models.Model):
    name = models.CharField(blank=False, max_length=64)

class Refrence(models.Model):
    name = models.CharField(blank=False, max_length=255)

class Article(models.Model):
    title = models.CharField(blank=False, max_length=255)
    body = models.TextField(blank=False)
    resume = models.TextField(blank=False)
    url = models.FileField(blank=False, upload_to='uploaded_articles')

    authors = models.ManyToManyField(Author)
    institutions = models.ManyToManyField(Institution)
    keywords = models.ManyToManyField(Keyword)
    refrences = models.ManyToManyField(Refrence)

    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        """Meta options."""

        ordering = ["created_at"]

    @property
    def authors_indexing(self):
        """Tags for indexing.

        Used in Elasticsearch indexing.
        """
        return [key.name for key in self.authors.all()]

    @property
    def institutions_indexing(self):
        """Tags for indexing.

        Used in Elasticsearch indexing.
        """
        return [key.name for key in self.institutions.all()]

    @property
    def keywords_indexing(self):
        """Tags for indexing.

        Used in Elasticsearch indexing.
        """
        return [key.name for key in self.keywords.all()]

    @property
    def refrences_indexing(self):
        """Tags for indexing.

        Used in Elasticsearch indexing.
        """
        return [key.name for key in self.refrences.all()]
