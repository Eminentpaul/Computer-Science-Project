# Generated by Django 5.1.7 on 2025-07-18 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_rename_lecturer_staff'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='staff',
            options={'ordering': ['status', 'full_name'], 'verbose_name': 'Staff'},
        ),
    ]
