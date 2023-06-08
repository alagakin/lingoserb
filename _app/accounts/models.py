from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError


def validate_image_size(image):
    max_size = 1 * 1024 * 1024  # 2 MB

    if image.size > max_size:
        raise ValidationError(
            f"The maximum file size allowed is 1 MB.")


class CustomUser(AbstractUser):
    picture = models.ImageField(upload_to='media', blank=True,
                                validators=[validate_image_size])

    LANG_CHOICES = [
        ('ru', 'Russian'),
        ('en', 'English'),
    ]
    lang = models.CharField(max_length=3, choices=LANG_CHOICES, null=False,
                            default='ru')

    def __str__(self):
        return self.username
