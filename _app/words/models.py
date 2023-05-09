from django.db import models


class Word(models.Model):
    title = models.CharField(max_length=255)
    part = models.CharField(max_length=32)
