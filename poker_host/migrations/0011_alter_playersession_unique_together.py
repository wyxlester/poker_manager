# Generated by Django 4.2.7 on 2023-12-20 18:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("poker_host", "0010_session_duration_hours_session_duration_minutes"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="playersession",
            unique_together={("player_id", "session_id")},
        ),
    ]
