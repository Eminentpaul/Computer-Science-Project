# Generated by Django 5.1.7 on 2025-07-19 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_excos_year'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Hall',
            new_name='Class_Timetable',
        ),
        migrations.AlterModelOptions(
            name='excos',
            options={'ordering': ['-year'], 'verbose_name_plural': 'Excos'},
        ),
        migrations.AlterModelOptions(
            name='staff',
            options={'ordering': ['status'], 'verbose_name_plural': 'Staff List'},
        ),
    ]
