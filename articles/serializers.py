from collections import OrderedDict
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.fields import get_error_detail, set_value, SkipField
from .models import Article, Author, Keyword, Institution, Refrence

import re

from bs4 import BeautifulSoup
from grobid.client import GrobidClient

class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = (
            'id', 'name'
        )

class InstitutionSerializer(ModelSerializer):
    class Meta:
        model = Institution
        fields = (
            'id', 'name'
        )

class RefrenceSerializer(ModelSerializer):
    class Meta:
        model = Refrence
        fields = (
            'id', 'name'
        )

class KeywordSerializer(ModelSerializer):
    class Meta:
        model = Refrence
        fields = (
            'id', 'name'
        )

class ArticleSerializer(ModelSerializer):
    authors = AuthorSerializer(read_only=True, many=True)
    institutions = InstitutionSerializer(read_only=True, many=True)
    keywords = KeywordSerializer(read_only=True, many=True)
    refrences = RefrenceSerializer(read_only=True, many=True)

    reader = None

    class Meta:
        model = Article
        read_only_fields_for_everyone = ('id', 'pdf', 'created_at', 'updated_at')
        fields = read_only_fields_for_everyone + (
            'title', 'body', 'resume', 'authors', 'keywords', 'institutions', 'refrences'
        )
        read_only_fields = ('title', 'body', 'resume', 'authors', 'keywords', 'institutions', 'refrences', 'created_at',
            'updated_at')

    def to_internal_value(self, data):
        errors = OrderedDict()
        req_data = data.copy()

        for ro_field in self.Meta.read_only_fields_for_everyone:
            if (ro_field in req_data):
                errors[ro_field] = 'field is readonly'
                if (self.instance is not None and ro_field != 'pdf'):
                    req_data.pop(ro_field, None)

        read_only_fields = super()._readable_fields
        ret = super().to_internal_value(req_data)

        if (self.instance is None):
            return ret

        if not errors:
            for field in read_only_fields:
                if not(field.field_name in data):
                    continue

                """ Fake those so that validators are run. """
                field.read_only = False
                field.editable = True
                field.required = True

                primitive_value = field.get_value(data)
                validate_method = getattr(self, 'validate_' + field.field_name, None)
                try:
                    validated_value = field.run_validation(primitive_value)
                    if validate_method is not None:
                        validated_value = validate_method(validated_value)
                except ValidationError as exc:
                    errors[field.field_name] = exc.detail
                except DjangoValidationError as exc:
                    errors[field.field_name] = get_error_detail(exc)
                except SkipField:
                    print('skii')
                    pass
                else: set_value(ret, field.source_attrs, validated_value)

        if errors:
            raise ValidationError(errors)

        return ret
    
    def trim(self, text: str, seed='\n', remove_crlf_inbetween=True):
        res = re.findall(rf'[{seed}]+$|^[{seed}]+' + rf'|[\n\r]+' if remove_crlf_inbetween else '', string=text)
        for m in res:
            text = text.replace(m, '')
        return text
    
    def gorbid_scan(self, pdf: str):
        #TODO: find way to call the softwere directly as this slows down the process
        client = GrobidClient('http://127.0.0.1', 8070)
        res, status = client.serve('processFulltextDocument', pdf, teiCoordinates=[])

        assert(status == 200)

        # Parse the XML content
        soup = BeautifulSoup(markup=res.content, features='lxml-xml')
        header = soup.find('teiHeader')

        # this shoud never happen, atleast there is someting in the header
        assert(header is not None)

        title = header.find('titleStmt').find('title').get_text(strip=True)
        authors = []
        affiliations = set()
        refrences = []
        authors_soup = header.find_all('author') # make sure to target only the header
        
        for author in authors_soup:
            persName = author.find('persName')

            if (persName is None):
                continue

            name = persName.get_text(strip=True, separator=' ')
            authors.append(name)

        affiliations_soup = header.find_all('affiliation')
        for affiliation in affiliations_soup:
            #TODO: link each author with correspoding affiliation
            # this needs more research
            index_soup = affiliation.get('key', default=None)

            if (index_soup is None):
                continue

            org = affiliation.find('orgName')

            if (org is None):
                continue

            institution = affiliation.find('orgName', {'type': 'institution'})
            department = affiliation.find('orgName', {'type': 'department'})

            if (institution is None and department is None):
                continue

            institution_name = ''
            if (institution is not None):
                institution_name = institution.get_text(strip=True)
            if (department is not None):
                institution_name = f'{institution_name} {department.get_text(strip=True)}'

            affiliations.add(institution_name.strip())

        refrences_soup = soup.find('listBibl')
        for refrence in refrences_soup:
            if isinstance(refrence, str):
                continue

            # needs improvment
            refrences.append(refrence.get_text(strip=True, separator=' '))

        # needs improvment
        keywords = None
        keywords_soup = header.find('keywords')
        if (keywords_soup is not None):
            keywords = keywords_soup.get_text()

        # needs improvment
        abstract = None
        abstract_soup = header.find('abstract')
        if (abstract_soup is not None):
            abstract = abstract_soup.get_text()

        body_soup = soup.find('body')

        assert(body_soup is not None)

        body_heads = body_soup.find_all('head', attrs={'n': True})
        body = ''
        for section_head in body_heads:
            number = section_head.get('n')
            section_title = section_head.get_text()
            p = f'{number} {section_title}\n'
            for child in section_head.parent.children:
                if (child is section_head):
                    continue
                p += '\n'
                p += child.get_text()

            body += p

        return (title, authors, abstract, keywords, body, affiliations, refrences)

    def create(self, validated_data):
        article = Article.objects.create(**validated_data)

        title, authors, abstract, keywords, body, affiliations, refrences = self.gorbid_scan(article.pdf.path)
        print(keywords)

        article.title = title
        article.resume = abstract
        for name in authors:
            author = Author.objects.filter(name=name).first()
            if (author is None):
                author = Author(name=name)
                author.save()
            article.authors.add(author)

        for name in affiliations:
            institution = Institution.objects.filter(name=name).first()
            if (institution is None):
                institution = Institution(name=name)
                institution.save()
            article.institutions.add(institution)

        for key in keywords.splitlines():
            #TODO: needs better approach
            if (len(key) > 50):
                continue
    
            key = self.trim(key, seed=r'\n\*\s\$')

            if (key == '' or len(key) < 2):
                continue

            keyword = Keyword.objects.filter(name=key).first()
            if keyword is None:
                keyword = Keyword(name=key)
                keyword.save()
            article.keywords.add(keyword)

        for name in refrences:
            refrence = Refrence.objects.filter(name=name).first()
            if (refrence is None):
                refrence = Refrence(name=name)
                refrence.save()
            article.refrences.add(refrence)

        article.body = body

        article.save()

        return article