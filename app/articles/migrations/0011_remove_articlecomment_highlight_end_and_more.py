# Generated by Django 4.1 on 2022-08-05 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0010_articlecomment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="articlecomment",
            name="highlight_end",
        ),
        migrations.RemoveField(
            model_name="articlecomment",
            name="highlight_start",
        ),
        migrations.RemoveField(
            model_name="articlecomment",
            name="highlight_text",
        ),
    ]