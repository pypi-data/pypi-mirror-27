# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-28 12:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('views', '0007_data_migration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='view',
            options={'ordering': ('key',), 'permissions': (('view_view', 'Can view View'),), 'verbose_name': 'View', 'verbose_name_plural': 'Views'},
        ),
    ]
