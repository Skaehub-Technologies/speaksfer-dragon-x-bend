# Generated by Django 4.0.6 on 2022-07-22 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0006_alter_article_article_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="article_id",
            field=models.UUIDField(
                default="8cc149fa405641c8819d4c7220c172bc",
                editable=False,
                unique=True,
            ),
        ),
    ]