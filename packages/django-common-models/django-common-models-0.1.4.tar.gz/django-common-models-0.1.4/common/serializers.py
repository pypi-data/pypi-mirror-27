# coding: utf-8
from rest_framework import serializers


class LinkSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    def get_links(self, obj):
        raise NotImplementedError
