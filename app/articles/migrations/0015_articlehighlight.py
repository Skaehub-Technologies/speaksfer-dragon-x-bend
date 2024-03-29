# Generated by Django 4.1 on 2022-08-08 12:31

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("articles", "0014_merge_20220808_0856"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArticleHighlight",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "highlight_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "highlight_start",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "highlight_end",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                ("highlight_text", models.TextField(blank=True, null=True)),
                ("comment", models.TextField()),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="articles.article",
                    ),
                ),
                (
                    "highlighter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
