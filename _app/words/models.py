from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from learn_serbian.utils import transliterate


class Word(models.Model):
    title = models.CharField(max_length=255)
    part = models.CharField(max_length=32)


@receiver(pre_save, sender=Word)
def word_pre_save(sender, instance, **kwargs):
    instance.title = transliterate(instance.title)

    return instance


class Translation(models.Model):
    title = models.CharField(max_length=255)
    LANG_CHOICES = [
        ('ru', 'Russian'),
        ('eng', 'English'),
    ]
    lang = models.CharField(max_length=3, choices=LANG_CHOICES)
    word = models.ForeignKey(Word, related_name='translations',
                             on_delete=models.CASCADE)
