# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-20 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raghav', '0009_auto_20160219_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numberlist',
            name='number',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]