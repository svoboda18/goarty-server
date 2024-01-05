from collections import OrderedDict
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.fields import (get_error_detail, set_value, SkipField)
from .models.article import Article

from .models.article import Author
from .models.article import Keyword
from .models.article import Institution
from .models.article import Refrence

import pypdf, re

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
        fields = (
            'id', 'title', 'body', 'resume', 'url', 'authors', 'keywords', 'institutions', 'refrences'
        )
        read_only_fields = ('title', 'body', 'resume', 'authors', 'keywords', 'institutions', 'refrences')

    def to_internal_value(self, data):
        errors = OrderedDict()
        req_data = data.copy()
        read_only_for_everyone = ['id', 'url']

        for ro_field in read_only_for_everyone:
            if (ro_field in req_data):
                errors[ro_field] = 'field is readonly'
                if (self.instance is not None):
                    req_data.pop(ro_field, None)

        #TODO: check user role
        user = self.context['request'].user

        read_only_fields = super()._readable_fields
        ret = super().to_internal_value(req_data)
        
        if (self.instance is None):
            return ret

        if not errors:
            for field in read_only_fields:
                if not(field.field_name in data):
                    continue

                field.read_only = False
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

    def validate(self, validated_data):
        if (self.instance is not None):
            return validated_data

        pdf = validated_data['url']
        if (pdf is None or
            pdf.name.split('.')[-1] != 'pdf' or 
            pdf.content_type != 'application/pdf'):
            raise ValidationError("wrong file type")

        return validated_data

    def create(self, validated_data):
        pdf = validated_data['url']
        article = Article.objects.create(**validated_data)

        reader = pypdf.PdfReader(pdf.file)

        article.title = reader.metadata.title
        author = Author.objects.filter(name=reader.metadata.author).first()
        if (author is None):
            author = Author(name=reader.metadata.author)
            author.save()
        article.authors.add(author)

        body = ''
        for page in reader.pages:
            text = page.extract_text()
            keywords = re.search(r"keywords\s*?:?\s*?([^.]+)", text, re.I | re.M)
            if (keywords is not None):
                for key in [*keywords.groups(0)[0].split(','), *keywords.groups(0)[0].split(';')]:
                    keyword = Keyword.objects.filter(name=key.strip()).first()
                    if keyword is None:
                        keyword = Keyword(name=key.strip())
                        keyword.save()
                    article.keywords.add(keyword)

            references = re.search(r"r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\s*:?(([^.]+\.)+)", text, re.I | re.M)
            if (references is not None):
                references_groups = references.groups()
                for i in range(len(references_groups)):
                    reference = references_groups[i]
                    if i < len(references_groups) - 1:
                        reference = reference.replace(references_groups[i+1], '')
                    ref = Refrence.objects.filter(name=reference.strip('\n\r ')).first()
                    if ref is None:
                        ref = Refrence(name=reference.strip('\n\r '))
                        ref.save()
                    article.refrences.add(ref)
            body+= text
        article.body = body

        article.save()

        return article