# coding: utf-8
from __future__ import unicode_literals

import json
import boto3
from django.contrib.auth.models import User
from rest_framework import serializers
from user_profile.models import Profile


class UserSerializer(serializers.ModelSerializer):
    """
     Only user serializer
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'email', 'last_login', 'date_joined')

class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile serializer, nest by UserProfileSerializer
    this serializer for single profile edit or get aws options
    """

    class Meta:
        model = Profile
        fields = (
            'id', 'org_name', 'org_address', 'contract', 'phone_number',
            'access_key_id', 'secret_access_key', 'region', 'options',
            'external_id', 'role_arn', 'bucket', 'base'
            )


class ChangePasswordSerializer(serializers.Serializer):
    """
    for change password.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



class UserProfileSerializer(serializers.ModelSerializer):
    """
    user and profile serializer
    default serializer for CRUD
    """
    org_name = serializers.CharField(
        source='profile.org_name',
        trim_whitespace=True,
        allow_blank=True
    )
    org_address = serializers.CharField(
        source='profile.org_address',
        trim_whitespace=True,
        allow_blank=True
    )
    contract = serializers.CharField(
        source='profile.contract',
        trim_whitespace=True,
        allow_blank=True
    )
    org_name = serializers.CharField(
        source='profile.org_name',
        trim_whitespace=True,
        allow_blank=True
    )
    phone_number = serializers.CharField(
        source='profile.phone_number',
        trim_whitespace=True,
        allow_blank=True
    )
    access_key_id = serializers.CharField(
        source='profile.access_key_id',
        trim_whitespace=True,
        allow_blank=True
    )
    secret_access_key = serializers.CharField(
        source='profile.secret_access_key',
        trim_whitespace=True,
        allow_blank=True
    )
    region = serializers.CharField(
        source='profile.region',
        trim_whitespace=True,
        allow_blank=True
    )
    options = serializers.CharField(
        source='profile.options',
        trim_whitespace=True,
        allow_blank=True
    )
    external_id = serializers.CharField(
        source='profile.external_id',
        trim_whitespace=True,
        allow_blank=True
    )
    role_arn = serializers.CharField(
        source='profile.role_arn',
        trim_whitespace=True,
        allow_blank=True
    )
    bucket = serializers.CharField(
        source='profile.bucket',
        trim_whitespace=True,
        allow_blank=True
    )
    base = serializers.CharField(
        source='profile.base',
        trim_whitespace=True,
        allow_blank=True
    )


    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'email', 'last_login', 'date_joined', 'is_staff',
            'org_name', 'org_address', 'contract', 'phone_number',
            'access_key_id', 'secret_access_key', 'region', 'options',
            'external_id', 'role_arn', 'bucket', 'base'
        )
    

    
