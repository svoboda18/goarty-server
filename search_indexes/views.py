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
    LOOKUP_QUERY_CONTAINS
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    CompoundSearchFilterBackend,
    FacetedSearchFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination


class AriticleViewSet(BaseDocumentViewSet):
    serializer_class = ArticleDocumentSerializer
    permission_classes = (AllowAny)
    parser_classes = (MultiPartParser, FormParser,)

    # TODO: needs clean-up
    document = ArticleDocument
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        FacetedSearchFilterBackend
    ]
    search_fields = (
        'title',
        'body',
        'authors',
        'keywords',
    )

    filter_fields = {
        'created_at': {
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
        'created_at': {
            'field': 'created_at',
            'facet': DateHistogramFacet,
            'enabled': True,
            'options': {
                'interval': 'day',  # Adjust the interval as needed
            },
        },
    }
    
    ordering_fields = {
        'created_at': 'created_at',
    }
    ordering = ('created_at',)
