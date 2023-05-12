# Generated by Django 4.2.1 on 2023-05-11 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0006_texttranslation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='word',
            name='categories',
            field=models.ManyToManyField(related_name='words', to='words.category'),
        ),
    ]