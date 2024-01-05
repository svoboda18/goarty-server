from random import randint
from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from ..models.article import Article
from ..models.author import Author
from ..models.keyword import Keyword
from ..models.institution import Institution
from ..models.refrence import Refrence

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
    url = Faker('url')
    resume = Faker('text')

    @post_generation
    def relations(self, create, extracted, **kwargs):
        if create:
            self.authors.add(*AuthorFactory.create_batch(randint(1, 10)))
            self.keywords.add(*KeywordFactory.create_batch(randint(1, 10)))
            self.institutions.add(*InstitutionFactory.create_batch(randint(1, 10)))
            self.refrences.add(*RefrenceFactory.create_batch(randint(1, 10)))

    class Meta:
        model = Article