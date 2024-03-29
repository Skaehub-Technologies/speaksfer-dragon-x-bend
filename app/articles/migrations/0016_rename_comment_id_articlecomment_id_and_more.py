# Generated by Django 4.1 on 2022-08-11 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0015_articlehighlight"),
    ]

    operations = [
        migrations.RenameField(
            model_name="articlecomment",
            old_name="comment_id",
            new_name="id",
        ),
        migrations.RenameField(
            model_name="articlehighlight",
            old_name="highlight_id",
            new_name="id",
        ),
        migrations.AlterField(
            model_name="articlehighlight",
            name="highlight_end",
            field=models.PositiveIntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="articlehighlight",
            name="highlight_start",
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="articlehighlight",
            name="highlight_text",
            field=models.TextField(default="The story of african highlands"),
            preserve_default=False,
        ),
    ]
