from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers


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
