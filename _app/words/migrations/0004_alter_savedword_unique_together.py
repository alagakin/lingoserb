# Generated by Django 4.2.1 on 2023-05-10 14:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('words', '0003_savedword'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='savedword',
            unique_together={('user', 'word')},
        ),
    ]
