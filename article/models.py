from django.db import models
from django.core.validators import FileExtensionValidator


class Author(models.Model):
    name = models.CharField(blank=False, max_length=255)


class Institution(models.Model):
    name = models.CharField(blank=False, max_length=255)


class Keyword(models.Model):
    name = models.CharField(blank=False, max_length=64)


class Refrence(models.Model):
    name = models.CharField(blank=False, max_length=255)


# Characters modified counter
class CharCount(models.Model):
    count = models.IntegerField(default=0)


class Article(models.Model):
    title = models.CharField(blank=False, max_length=255)
    body = models.TextField(blank=False)
    resume = models.TextField(blank=False)
    pdf = models.FileField(
        blank=False,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        upload_to="uploaded_articles",
    )

    authors = models.ManyToManyField(Author, related_name="articles")
    institutions = models.ManyToManyField(Institution, related_name="articles")
    keywords = models.ManyToManyField(Keyword, related_name="articles")
    refrences = models.ManyToManyField(Refrence, related_name="articles")

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
