from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserDetailsSerializer(serializers.ModelSerializer):
    """User model w/o password."""
    class Meta:
        model = get_user_model()
        fields = ['pk', 'email']
        read_only_fields = ['pk']
