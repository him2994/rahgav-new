# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-28 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raghav', '0012_failednumbers'),
    ]

    operations = [
        migrations.AddField(
            model_name='failednumbers',
            name='discription',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='failednumbers',
            name='patent_number',
            field=models.CharField(default='', max_length=255),
        ),
    ]
