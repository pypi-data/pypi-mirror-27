# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-15 14:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_additional_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalfieldvalue',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_values', to=settings.AUTH_USER_MODEL),
        ),
    ]
