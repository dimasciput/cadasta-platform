# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-10 17:13
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaires', '0009_set_question_option_index_field_properties'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalquestion',
            name='label_xlat',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='historicalquestiongroup',
            name='label_xlat',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='historicalquestionnaire',
            name='default_language',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='historicalquestionoption',
            name='label_xlat',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='question',
            name='label_xlat',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='questiongroup',
            name='label_xlat',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='default_language',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='questionoption',
            name='label_xlat',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
