from django.db import models
from learn_serbian import settings
from words.models import Word, Text


class Topic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to=settings.MEDIA_ROOT, null=True,
                                blank=True)
    words = models.ManyToManyField(Word, related_name='topics',
                                   blank=True)
    texts = models.ManyToManyField(Text, related_name='topics',
                                   blank=True)

    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               related_name='subtopics', blank=True,
                               null=True)

    @property
    def words_count(self):
        return self.words.count()

    def __str__(self):
        return self.title


class TopicTranslation(models.Model):
    title = models.CharField(max_length=255)
    LANG_CHOICES = [
        ('ru', 'Russian'),
        ('en', 'English'),
    ]
    lang = models.CharField(max_length=3, choices=LANG_CHOICES)
    topic = models.ForeignKey(Topic, related_name='translations',
                              on_delete=models.CASCADE)
