# Generated by Django 4.1 on 2022-08-08 09:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "articles",
            "0011_merge_0010_article_reading_time_0010_articleratings",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="favourited",
        ),
        migrations.AddField(
            model_name="article",
            name="favourite",
            field=models.ManyToManyField(
                blank=True, related_name="likes", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="unfavourite",
            field=models.ManyToManyField(
                blank=True,
                related_name="dislikes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
