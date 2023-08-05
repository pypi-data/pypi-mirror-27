# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-14 12:13
from __future__ import unicode_literals

try:
    import rdmo.core.models
except ImportError:
    import rdmo.core.models

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0006_permissions_removed'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.SlugField()),
                ('type', models.CharField(choices=[('text', 'Text'), ('textarea', 'Textarea')], max_length=11)),
                ('text_en', models.CharField(max_length=256)),
                ('text_de', models.CharField(max_length=256)),
                ('help_en', models.TextField(blank=True, help_text='Enter a help text to be displayed next to the input element', null=True)),
                ('help_de', models.TextField(blank=True, help_text='Enter a help text to be displayed next to the input element', null=True)),
                ('required', models.BooleanField()),
            ],
            options={
                'ordering': ('key',),
                'verbose_name': 'Additional field',
                'verbose_name_plural': 'Additional fields',
            },
            bases=(models.Model, rdmo.core.models.TranslationMixin),
        ),
        migrations.CreateModel(
            name='AdditionalFieldValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=256)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='accounts.AdditionalField')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_fields', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('user', 'field'),
                'verbose_name': 'Additional field value',
                'verbose_name_plural': 'Additional field values',
            },
        ),
        migrations.DeleteModel(
            name='DetailKey',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
