# Generated by Django 5.1.7 on 2025-04-14 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_notification_saveitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='save_count',
            field=models.IntegerField(default=0),
        ),
    ]
