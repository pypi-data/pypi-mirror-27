# -*- coding: utf-8 -*-
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from . import models, serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """A simple ViewSet for viewing Users."""

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'username'
