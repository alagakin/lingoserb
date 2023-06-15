from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import ProfileSerializer
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


class ProfileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        profile = get_user_model().objects.get(id=request.user.id)
        serializer = ProfileSerializer(profile, data=request.data,
                                       context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        profile = get_user_model().objects.get(id=request.user.id)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_CALLBACK_URL
    client_class = OAuth2Client
