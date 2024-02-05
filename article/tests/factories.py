from random import randint
from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from ..models import Article, Author, Keyword, Institution, Refrence

class AuthorFactory(DjangoModelFactory):
    name = Faker('name')

    class Meta:
        model = Author

class KeywordFactory(DjangoModelFactory):
    name = Faker('word')

    class Meta:
        model = Keyword

class InstitutionFactory(DjangoModelFactory):
    name = Faker('company')

    class Meta:
        model = Institution

class RefrenceFactory(DjangoModelFactory):
    name = Faker('company')

    class Meta:
        model = Refrence

class ArticleFactory(DjangoModelFactory):
    title = Faker('text')
    body = Faker('text')
    pdf = Faker('name')
    resume = Faker('text')

    @post_generation
    def relations(self, create, extracted, **kwargs):
        if create:
            n = randint(1, 2)
            self.authors.add(*AuthorFactory.create_batch(n))
            self.keywords.add(*KeywordFactory.create_batch(n))
            self.institutions.add(*InstitutionFactory.create_batch(n))
            self.refrences.add(*RefrenceFactory.create_batch(n))

    class Meta:
        model = Article