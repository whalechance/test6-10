# Generated by Django 4.2 on 2023-06-10 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("photo", "0004_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="photopost",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=1, verbose_name="作成日時"
            ),
            preserve_default=False,
        ),
    ]
