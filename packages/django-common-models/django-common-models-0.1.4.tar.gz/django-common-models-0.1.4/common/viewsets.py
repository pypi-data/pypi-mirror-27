# coding: utf-8
from django.db.models import ProtectedError
from rest_framework import authentication, permissions, filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework_filters.backends import DjangoFilterBackend


class DefaultViewSetMixIn(object):

    '''Default options for viewsets and serializers'''
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permission_classes = (
        permissions.DjangoModelPermissions,
    )

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

    def destroy(self, request, pk=None):
        try:
            return super(DefaultViewSetMixIn, self).destroy(request, pk)
        except ProtectedError:
            return Response('Cannot delete object because of protected foreign key relation',
                            status=status.HTTP_409_CONFLICT)
