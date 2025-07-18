# Generated by Django 5.1.7 on 2025-07-10 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_lecturer_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Labs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='Labs')),
            ],
        ),
        migrations.AlterModelOptions(
            name='lecturer',
            options={'ordering': ['status', 'full_name']},
        ),
    ]
