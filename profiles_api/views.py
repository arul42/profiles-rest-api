from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions


class HelloApiView(APIView):
    """Test Api View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Return a list of API Views"""
        an_apiview = [
        'uses methods (Get, Put, Post, Patch, delete)',
        'similarly like django traditional views',
        'gives you most control over the application',
        'Is mapped manulay to the url',
        ]

        return Response({'message':'Hello World', 'an_apiview': an_apiview})

    def post(self, request):
        """Create Hello message with our names"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """Updating all the content"""
        return Response({'message': 'PUT'})

    def patch(self, request, pk=None):
        """Update only partial contents"""
        return Response({'message': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete content"""
        return Response({'message': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Return Lists"""
    serializer_class = serializers.HelloSerializer
    def list(self, request):
        a_viewset = [
        'uses methods (Get, Put, Post, Patch, delete)',
        'similarly like django traditional views',
        'gives you most control over the application',
        'Is mapped manulay to the url',
        ]
        return Response({'message': 'Hello', 'a_viewset':a_viewset})

    def create(self, request):
        """Create New List"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Get single Data based on ID"""
        return Response({'http_method':'GET'})

    def update(self, request, pk=None):
        """update one complete data based on id"""
        return Response({'http_method':'UPDATE'})

    def partial_update(self, request, pk=None):
        """update some field of one data based on id"""
        return Response({'http_method':'Partial_update'})

    def destroy(self, request, pk=None):
        """Delete one record"""
        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating the profile"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle Creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handle creating reading updating feeds"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticatedOrReadOnly
    )


    def perform_create(self, serializer):
        """Sets the user profile ot the logged in user"""
        serializer.save(user_profile=self.request.user)
