# coding: utf-8
from __future__ import unicode_literals
from rest_framework import viewsets, response, status
from rest_framework.decorators import detail_route
from django.contrib.auth.models import User
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.permissions_helper import IsAdminOrIsSelf
from user_profile.serializers import (
    UserSerializer, ProfileSerializer, UserProfileSerializer, 
    ChangePasswordSerializer, AWSCredentialsSerializer)
from user_profile.models import Profile

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    Change password
    Create user
    Edit profile
    """
    queryset = User.objects.select_related().all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAdminOrIsSelf,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @detail_route(methods=['post'])
    def set_password(self, request, *args, **kwargs):
        """
        check old password and set new password
        """
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data['old_password']
            if not user.check_password(old_password):
                return response.Response(
                    serializer.errors,
                    status=status.HTTP_401_UNAUTHORIZED
                )
            new_password = serializer.data['new_password']
            user.set_password(new_password)
            user.save()
            return response.Response(status=status.HTTP_200_OK)
        else:
            return response.Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )


    def perform_create(self, serializer):
        if 'profile' in serializer.validated_data:
            # pop profile's data,
            profile_data = serializer.validated_data.pop('profile')
            user = User.objects.create_user(**serializer.data)
            # create profile
            profile_serializer = ProfileSerializer(data=profile_data)
            profile_serializer.is_valid()
            profile_serializer.save(user=serializer.instance)

    def perform_update(self, serializer):
        user = self.get_object()
        profile = user.profile

        if 'profile' in serializer.validated_data:
            # pop profile's data,
            profile_data = serializer.validated_data.pop('profile')
            profile_serializer = ProfileSerializer(instance=profile, data=profile_data, partial=True)
            if profile_serializer.is_valid():
                profile_serializer.save()
        # save user
        if serializer.validated_data:
            serializer.save()