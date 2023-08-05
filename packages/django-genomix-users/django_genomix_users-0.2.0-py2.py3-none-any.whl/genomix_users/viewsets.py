# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from . import models, serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """A simple ViewSet for viewing Users."""

    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'username'


class ProfileViewSet(viewsets.ModelViewSet):
    """A simple ViewSet for viewing User Profiles."""

    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'user__username'
    http_method_names = ['get', 'put', 'patch', 'options', 'head']
