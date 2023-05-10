from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from learn_serbian.utils import transliterate


class Word(models.Model):
    title = models.CharField(max_length=255)
    part = models.CharField(max_length=32)

    def __str__(self):
        return self.title


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

    def __str__(self):
        return self.title


class SavedWord(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='saved',
                             on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    last_repetition = models.DateTimeField(null=True, blank=True)
    repetition_count = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.word) + ' - ' + str(self.user)

    class Meta:
        unique_together = ['user', 'word']
