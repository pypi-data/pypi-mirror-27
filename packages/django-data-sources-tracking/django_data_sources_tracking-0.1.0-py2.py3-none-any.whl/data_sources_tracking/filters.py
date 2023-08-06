# -*- coding: utf-8 -*-
from django.db.models import Q

import django_filters

from . import choices, models


class FileFilter(django_filters.rest_framework.FilterSet):

    file_type = django_filters.CharFilter(
        label='File Type',
        method='filter_file_type',
    )

    class Meta:
        model = models.File
        fields = [
            'name',
            'description',
            'url',
            'path',
            'active',
            'type',
            'file_type',
            'active',
            'relative_path',
        ]

    def filter_file_type(self, queryset, name, value):
        return queryset.filter(Q(type=getattr(choices.FILE_TYPES, value.lower())))
