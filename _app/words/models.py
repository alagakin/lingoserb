from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from learn_serbian import settings
from learn_serbian.utils import transliterate


class Text(models.Model):
    content = models.TextField()

    @property
    def words_count(self):
        return self.words.count()

    @property
    def translations_count(self):
        return self.translations.count()

    def __str__(self):
        return self.content[0:20] + '...'


@receiver(pre_save, sender=Text)
def word_pre_save(sender, instance, **kwargs):
    instance.content = transliterate(instance.content)

    return instance


class TextTranslation(models.Model):
    content = models.TextField()
    LANG_CHOICES = [
        ('ru', 'Russian'),
        ('en', 'English'),
    ]
    lang = models.CharField(max_length=3, choices=LANG_CHOICES, null=False)
    text = models.ForeignKey(Text, related_name='translations',
                             on_delete=models.CASCADE)

    @property
    def preview(self):
        return self.content[0:20] + '...'

    @property
    def words_count(self):
        return self.text.words_count

    def __str__(self):
        return self.preview


class Tag(models.Model):
    title = models.CharField(max_length=255)


class Word(models.Model):
    title = models.CharField(max_length=255)
    part = models.CharField(max_length=32)
    texts = models.ManyToManyField(Text, related_name='words')
    tags = models.ManyToManyField(Tag, related_name='words')
    s3_id = models.CharField(max_length=16, null=True, blank=True)

    @property
    def texts_count(self):
        return self.texts.count()

    @property
    def audio_link(self):
        if not self.s3_id:
            return None
        else:
            return f'https://{settings.S3_BUCKET_NAME}.s3.{settings.S3_REGION}.amazonaws.com/audio/{self.s3_id}.mp3'

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
        ('en', 'English'),
    ]
    lang = models.CharField(max_length=3, choices=LANG_CHOICES)
    word = models.ForeignKey(Word, related_name='translations',
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.title
