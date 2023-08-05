# -*- coding: utf-8 -*-
from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Users."""
    class Meta:
        model = models.User
        fields = (
            'id', 'username', 'email',
            'first_name', 'last_name',
            'is_staff', 'is_active', 'is_superuser',
            'last_login', 'date_joined',
        )
