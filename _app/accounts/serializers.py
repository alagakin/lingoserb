from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer


class CustomUserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(required=True)  # Add this line

    def perform_create(self, serializer):
        email = serializer.get('email')
        if email and self.user_exists(email):
            raise serializers.ValidationError({'email': ['Email address is already in use.']})
        return super().perform_create(serializer)

    def user_exists(self, email):
        return get_user_model().objects.filter(email=email).exists()

    class Meta(UserCreateSerializer.Meta):
        fields = ('email', 'username', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('picture', 'lang',)

    def get_picture(self, obj):
        request = self.context.get('request')
        if obj.picture:
            # Get the current site's domain and protocol
            current_site = get_current_site(request)
            protocol = 'https' if request.is_secure() else 'http'
            domain = current_site.domain

            # Construct the complete URL for the picture field
            picture_url = f'{protocol}://{domain}{obj.picture.url}'
            return picture_url
        else:
            return None
