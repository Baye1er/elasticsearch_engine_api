# Create your views here.
from django.http import JsonResponse
import requests
import json
from .models import *

from .documents import *
from .serializers import *

from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    CompoundSearchFilterBackend,
)


def generate_random_data():
    url = 'https://newsapi.org/v2/everything?domains=wsj.com&apiKey=539209db6c4645ae816cdf829d4452da'
    r = requests.get(url)
    payload = json.loads(r.text)
    for data in payload.get('articles'):
        ElasticItem.objects.create(
            title=data.get('title'),
            content=data.get('description')
        )


def index(request):
    generate_random_data()
    return JsonResponse({'status': 200})


class PublisherDocumentView(DocumentViewSet):
    document = NewsDocument
    serializer_class = NewsDocumentSerializer
    lookup_field = 'first_name'
    fielddata = True
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]

    search_fields = (
        'title',
        'content',
    )
    multi_match_search_fields = (
        'title',
        'content',
    )
    filter_fields = {
        'title': 'title',
        'content': 'content',
    }
    ordering_fields = {
        'id': None,
    }
    ordering = ('id',)


