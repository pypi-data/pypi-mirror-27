# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-11 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('views', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='view',
            name='template',
            field=models.TextField(blank=True, null=True),
        ),
    ]
