# coding: utf-8
from rest_framework_filters import FilterSet
from django.contrib.contenttypes.models import ContentType


class ContentTypeFilter(FilterSet):

    class Meta:
        model = ContentType
        fields = {
            'model': ['exact', 'icontains'],
        }
