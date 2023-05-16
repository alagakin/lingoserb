from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
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

    @property
    def texts_count(self):
        return self.texts.count()

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Word)
def word_pre_save(sender, instance, **kwargs):
    instance.title = transliterate(instance.title)

    return instance


class Category(models.Model):
    title = models.CharField(max_length=255)
    # todo lang?
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='pictures/', null=True, blank=True)
    words = models.ManyToManyField(Word, related_name='categories')
    texts = models.ManyToManyField(Text, related_name='categories')

    class Meta:
        verbose_name_plural = "categories"

    @property
    def words_count(self):
        return self.words.count()

    def __str__(self):
        return self.title





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
