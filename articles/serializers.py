from collections import OrderedDict
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.fields import get_error_detail, set_value, SkipField
from .models import Article, Author, Keyword, Institution, Refrence

import pypdf, re, pypdfium2

from py_pdf_parser.loaders import load_file
from py_pdf_parser.filtering import BoundingBox
#from py_pdf_parser.visualise import visualise

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

    def validate(self, attrs):
        if (self.instance is not None):
            return attrs

        pdf = attrs['pdf']
        if (pdf is None or
            pdf.name.split('.')[-1] != 'pdf' or 
            pdf.content_type != 'application/pdf'):
            raise ValidationError("wrong file type")

        return attrs
    
    def textify_section(self, section, sep='\n', ignore_first=True):
        return sep.join([elm.text() for elm in (section.elements.after(section.elements[0]) if ignore_first else section.elements)])

    def trim(self, text: str, seed='\n', remove_crlf_inbetween=True):
        res = re.findall(rf'[{seed}]+$|^[{seed}]+{ '|[\n\r]+' if remove_crlf_inbetween else '' }', string=text)
        for m in res:
            text = text.replace(m, '')
        return text

    def create(self, validated_data):
        article = Article.objects.create(**validated_data)

        FONT_MAPPING = {
            r"(\w{6}\+)?[\w-]+,(1[6789]|[2-3][0-9])": "title",
            r"(\w{6}\+)?[\w-]+,(10.0|9.8)": "author_inst_email",
            r"(\w{6}\+)?(Times-(Bold|Roman),12.0|[\w-]+,[89].[0-9])": "sub_title",
            r"(\w{6}\+)?Times-Roman,9.0": "text",
        }

        document = load_file(article.pdf.path, font_mapping=FONT_MAPPING, font_mapping_is_regex=True)

        pdf = pypdfium2.PdfDocument(article.pdf.path)
        version = pdf.get_version()  # get the PDF standard version
        n_pages = len(pdf)  # get the number of pages in the document
        page = pdf.get_page(0)

        textpage = page.get_textpage()
        title = textpage.get_text_bounded(left=40, bottom=678, right=580, top=718)
        title_lines = title.splitlines()
        title_box = document.elements.filter_by_text_contains(title_lines[0])[0].bounding_box
        title_bottom = (675 + title_box.y0) / 2
        authors_bottom = title_bottom - 20
        authors = textpage.get_text_bounded(left=90, bottom=authors_bottom, right=540, top=title_bottom - 3)
        institutions = textpage.get_text_bounded(left=95, bottom=title_bottom - 31
                                                 , right=540, top=authors_bottom - 2)

        print(title) 
        print('auuuth:')

        print(authors)
        print('instttt:')
        print(institutions)

        pot_auth_inst = document.elements.filter_by_font('author_inst_email')

        k = document.elements.filter_partially_within_bounding_box(BoundingBox(x0=80, x1=540, y0=709.5
                                                                                    , y1=720), page_number=1)
        l = document.elements.filter_partially_within_bounding_box(BoundingBox(x0=100, x1=520, y0=640
                                                                                    , y1=650), page_number=1)
        print(len(l))
        #visualise(document, elements=l)
        print(set(element.font for element in document.elements))
        #print(document.elements.filter_by_text_contains(r'Shivangi')[0].bounding_box)
        #print(document.elements.filter_by_text_contains(r'Features and Ensemble AI Model')[0].bounding_box)
        #print(document.elements.filter_by_text_contains(r'Khushbu')[0].font)

        if len(pot_auth_inst) == 1:
            pot_auth_inst_text = pot_auth_inst.extract_single_element().text()
        else:
            pot_auth_inst_text = '\n'.join([elm.text() for elm in pot_auth_inst])


        count = pot_auth_inst_text.count('@')
        print(count)
        #print(pot_auth_inst_text)
        authors = []
        institutions = []
        i = 0

        pot_auth_inst_text_array = pot_auth_inst_text.splitlines()

        for _ in range(count):
            authors.append(pot_auth_inst_text_array[i])
            institutions.append(pot_auth_inst_text_array[i+1])
            i+=2

        title = document.elements.filter_by_font('title').extract_single_element().text()

        sub_titles = document.elements.filter_by_font("sub_title")

        abstract_sub_title = (
            document.elements.filter_by_regex(r"^abstract(?:/s*)?", regex_flags=re.I)
            [0]
        )

        abstract_section = document.sectioning.create_section(
            name="abstract",
            start_element=abstract_sub_title,
            end_element=sub_titles.below(abstract_sub_title)[0],
            include_last_element=False,
        )

        keywords_sub_title = (
            document.elements.filter_by_regex(r"(keywords|index terms)", re.I)
            [0]
        )

        introduction_sub_title = (
            sub_titles
            .filter_by_regex(r"([1-9\w\s.:]+)?Introduction", regex_flags=re.I)
            .extract_single_element()
        )

        keywords_section = None

        #if (introduction_sub_title in document.elements.after(keywords_sub_title)):
        keywords_section = document.sectioning.create_section(
            name="keywords",
            start_element=keywords_sub_title,
            end_element=document.elements[keywords_sub_title._index + 1],
            include_last_element=False,
        )

        refrences_sub_title = (
            document.elements.filter_by_regex(r"([1-9\w\s.:]+)?references", re.I)
            [0]
        )

        body_section = document.sectioning.create_section(
            name="body",
            start_element=introduction_sub_title,
            end_element=refrences_sub_title,
            include_last_element=False,
        )

        refrences_section = document.sectioning.create_section(
            name="refrences",
            start_element=refrences_sub_title,
            end_element=document.elements[-1],
            include_last_element=False,
        )

        article.title = title
        article.resume = self.textify_section(abstract_section)
        for name in authors:
            name = self.trim(name, seed=r'\n\*\s\$')
            author = Author.objects.filter(name=name).first()
            if (author is None):
                author = Author(name=name)
                author.save()
            article.authors.add(author)

        for name in institutions:
            institution = Institution.objects.filter(name=name).first()
            if (institution is None):
                institution = Institution(name=name)
                institution.save()
            article.institutions.add(institution)

        keywords = keywords_sub_title.text() if keywords_section is None else keywords_section.elements[0].text()
        for key in keywords[9:].split(','):
            key = self.trim(key.strip())
            keyword = Keyword.objects.filter(name=key).first()
            if keyword is None:
                keyword = Keyword(name=key)
                keyword.save()
            article.keywords.add(keyword)

        pot_refrences = self.textify_section(refrences_section, ignore_first=False)
        refrences = []
        for ref in pot_refrences.splitlines():
            match = re.match(r'\[\d+\] (.*)', ref, re.I)
            if (match is not None):
                refrences.append(match.group(1))
        
        for name in refrences:
            refrence = Refrence.objects.filter(name=name).first()
            if (refrence is None):
                refrence = Refrence(name=name)
                refrence.save()
            article.refrences.add(refrence)

        article.body = self.textify_section(body_section, ignore_first=False)

        article.save()

        return article