# Generated by Django 5.0.6 on 2024-11-22 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_alter_like_unique_together_like_session_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='likes_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
