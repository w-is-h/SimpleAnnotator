# Generated by Django 2.2.3 on 2019-09-21 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotator', '0002_project_add_data_from'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='string_orig',
            field=models.TextField(blank=True, default=''),
        ),
    ]
