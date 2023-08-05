# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-03 11:30
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_options(apps, schema_editor):

    Option = apps.get_model('options', 'Option')

    for option in Option.objects.all():
        option.path = option.optionset.key + '/' + option.key
        option.save()


class Migration(migrations.Migration):

    dependencies = [
        ('options', '0008_option_path'),
    ]

    operations = [
        migrations.RunPython(migrate_options),
    ]
