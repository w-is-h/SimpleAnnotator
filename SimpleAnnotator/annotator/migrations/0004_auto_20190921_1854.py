# Generated by Django 2.2.3 on 2019-09-21 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotator', '0003_document_string_orig'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metaannotation',
            name='acc',
        ),
        migrations.RemoveField(
            model_name='metaannotation',
            name='validated',
        ),
    ]
