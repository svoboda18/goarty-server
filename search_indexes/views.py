from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from .documents import ArticleDocument
from .serializers import ArticleDocumentSerializer

from elasticsearch_dsl import DateHistogramFacet

from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_EXCLUDE,
    LOOKUP_QUERY_CONTAINS,
    SUGGESTER_TERM,
    SUGGESTER_PHRASE,
    SUGGESTER_COMPLETION
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    CompoundSearchFilterBackend,
    FacetedSearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination


class AriticleViewSet(DocumentViewSet):
    serializer_class = ArticleDocumentSerializer
    parser_classes = (MultiPartParser, FormParser,)

    document = ArticleDocument
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        FacetedSearchFilterBackend,
        SuggesterFilterBackend
    ]
    search_fields = (
        'title',
        'body',
        'authors',
        'keywords',
    )

    suggester_fields = {
        'title_suggest': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_TERM,
                SUGGESTER_PHRASE,
                SUGGESTER_COMPLETION,
            ],
            'options': {
                'size': 7,
                'skip_duplicates': True,
            },
        },
    }
    filter_fields = {
        'date': {
            'field': 'created_at',
            'lookups': [
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_LTE,
                LOOKUP_QUERY_LT,
            ],
        },
        'authors.raw': {
            'field': 'authors.raw',
            'lookups': [
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
            ],
        },
        'authors': {
            'field': 'authors',
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
                LOOKUP_QUERY_CONTAINS
            ],
        },

        'institutions': {
            'field': 'institutions',
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
                LOOKUP_QUERY_CONTAINS
            ],
        },
        'institutions.raw': {
            'field': 'institutions.raw',
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },

        'keywords': {
            'field': 'keywords',
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
                LOOKUP_QUERY_CONTAINS
            ],
        },
        'keywords.raw': {
            'field': 'keywords.raw',
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
    }
    faceted_search_fields = {
        'date': {
            'field': 'created_at',
            'facet': DateHistogramFacet,
            'enabled': True,
            'options': {
                'fixed_interval': '1d',
            },
        },
    }
    
    ordering_fields = {
        'date': 'created_at',
    }
    ordering = ('-date',)
