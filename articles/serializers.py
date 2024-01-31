from collections import OrderedDict
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.fields import get_error_detail, set_value, SkipField
from .models import Article, Author, Keyword, Institution, Refrence

import traceback, re

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
    
    def extarct_authors(self, soup):
        authors = []
        authors_soup = soup.find_all('author')

        for author in authors_soup:
            persName = author.find('persName')

            if (persName is None):
                continue

            forename = author.find('forename')
            surname = author.find('surname')

            if (forename is None or surname is None):
                continue

            # first and middle names could be the same node
            middle_name_tag = author.find('forename', {'type': 'middle'})
            middle_name = middle_name_tag.text if middle_name_tag else None

            authors.append(f"{forename.text}{f' {middle_name}' if middle_name else ''} {surname.text}")
        return authors
    
    def grobid_scan(self, pdf: str):
        #TODO: find way to call the softwere directly as this slows down the process
        # applies only to bigger pdf files
        client = GrobidClient('http://grobid', 8070)
        res, status = client.serve('processFulltextDocument', pdf, teiCoordinates=[])

        assert(status == 200)

        # Parse the XML content
        soup = BeautifulSoup(markup=res.content, features='lxml-xml')
        header = soup.find('teiHeader')

        # this shoud never happen, atleast there is someting in the header
        assert(header is not None)

        title = header.find('titleStmt').find('title').get_text(strip=True)
        authors = self.extarct_authors(header)
        affiliations = set()
        refrences = []

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

            institution_name = ' '.join(part.text for part in (institution, department) if part)

            affiliations.add(institution_name)

        refrences_soup = soup.find('listBibl')
        for refrence in refrences_soup.children:
            if isinstance(refrence, str):
                continue

            analytic = refrence.find('analytic')
            monogr = refrence.find('monogr')

            if (monogr is None):
                continue

            analytic_title = None
            if analytic is not None:
                analytic_title = analytic.find('title')
            monogr_title = monogr.find('title')
            publisher = monogr.find('publisher')

            if (monogr_title is None and
                analytic_title is None and
                publisher is None):
                continue

            reference_authors = ', '.join(self.extarct_authors(monogr if analytic is None else analytic))
            reference_note = f'{reference_authors}. ' if reference_authors else ''

            reference_note += ' '.join(text for text in (part.text for part in (analytic_title, monogr_title, publisher) if part) if text)

            if not reference_note:
                continue

            date = monogr.find('date', { 'type': 'published', 'when': True})
            issue = monogr.find('biblScope', { 'unit': 'issue'})
            page = monogr.find('biblScope', { 'unit': 'page', 'from': True, 'to': True})
            volume = monogr.find('biblScope', { 'unit': 'volume'})
            note = refrence.find('note')
            idno = monogr.find('idno')

            reference_note += ' '
            reference_note += ', '.join(part.text for part in (date, volume, issue, note, idno) if part)

            if page:
                reference_note += f', {page.get("from")}-{page.get("to")}'

            refrences.append(reference_note + '.')

        # needs improvment
        keywords = None
        keywords_soup = header.find('keywords')
        if (keywords_soup is not None):
            keywords = keywords_soup.get_text()

        # needs more improvment
        abstract = None
        abstract_soup = header.find('abstract').find('div')
        if (abstract_soup is not None):
            abstract = abstract_soup.get_text()

        body_soup = soup.find('body')

        assert(body_soup is not None)

        body_divs = body_soup.find_all('div')
        body = ''
        for section_div in body_divs:
            section_head = section_div.find('head')
            number = section_head.get('n', None)
            section_title = section_head.get_text()
            p = ''
            if (number):
                p = f'{number} '
            p += section_title
            p += '\n'
            for child in section_div.children:
                if (child is section_head):
                    continue
                p += child.get_text(strip=True)
                p += '\n'
            body += p

        return (title, authors, abstract, keywords, body, affiliations, refrences)

    def create_if_needed_then_add(self, list, model, instance, rel_name):
        for name in list:
            obj = model.objects.filter(name=name).first()
            if (obj is None):
                obj = model(name=name)
                obj.save()
            field = getattr(instance, rel_name)
            field.add(obj)

    def create(self, validated_data):
        article = Article.objects.create(**validated_data)

        # t1 = time.time()
        try:
            title, authors, abstract, keywords, body, affiliations, refrences = self.grobid_scan(article.pdf.path)
        except Exception:
            exception_traceback = traceback.format_exc()

            article.delete()

            raise ValidationError({ 'detail': 'well, our backends are trying thier best!', 'stacktrace': exception_traceback.splitlines()}, code=400)
        # t2 = time.time()

        # print('grobid_scan took: ' + str(t2 - t1))

        article.title = title
        article.resume = abstract

        self.create_if_needed_then_add(authors, Author, article, 'authors')
        self.create_if_needed_then_add(affiliations, Institution, article, 'institutions')
        self.create_if_needed_then_add(refrences, Refrence, article, 'refrences')

        for name in keywords.splitlines():
            name = self.trim(name, seed=r'\n\*\s\$')
            sz = len(name)

            # TODO:?
            if (name == '' or sz < 2 or sz > 50):
                continue

            keyword = Keyword.objects.filter(name=name).first()
            if keyword is None:
                keyword = Keyword(name=name)
                keyword.save()
            article.keywords.add(keyword)

        article.body = body

        article.save()

        return article