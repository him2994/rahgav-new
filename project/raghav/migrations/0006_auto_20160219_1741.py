# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 17:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raghav', '0005_auto_20160219_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ruser',
            name='password',
        ),
        migrations.RemoveField(
            model_name='ruser',
            name='username',
        ),
    ]