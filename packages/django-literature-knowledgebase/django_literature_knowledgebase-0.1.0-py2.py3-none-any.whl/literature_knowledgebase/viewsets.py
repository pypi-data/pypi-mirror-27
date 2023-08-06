# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from . import filters, models, serializers


class ArticleViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Articles."""

    queryset = models.Article.objects.fast()
    serializer_class = serializers.ArticleSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = filters.ArticleFilter
