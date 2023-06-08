from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    picture = models.ImageField(upload_to='media', blank=True)

    LANG_CHOICES = [
        ('ru', 'Russian'),
        ('en', 'English'),
    ]
    lang = models.CharField(max_length=3, choices=LANG_CHOICES, null=False,
                            default='ru')

    def __str__(self):
        return self.username
