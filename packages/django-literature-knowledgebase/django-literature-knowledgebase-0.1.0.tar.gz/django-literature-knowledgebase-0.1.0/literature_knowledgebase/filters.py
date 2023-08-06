# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.db.models import Q

import django_filters

from . import choices, models


class ArticleFilter(django_filters.rest_framework.FilterSet):

    username = django_filters.CharFilter(
        method='filter_username',
        label='Username',
    )

    source = django_filters.CharFilter(
        method='filter_source',
        label='Source',
    )

    class Meta:
        model = models.Article
        fields = [
            'source',
            'identifier',
            'user',
            'active',
            'description',
        ]

    def filter_username(self, queryset, name, value):
        return queryset.filter(Q(user__username__iexact=value))

    def filter_source(self, queryset, name, value):
        sources = OrderedDict(choices.SOURCES)
        for key, key_value in sources.items():
            if key_value.strip().lower() == value.strip().lower():
                return queryset.filter(Q(source=key))
