# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-01-25 03:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_auto_20180124_2216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='created_date_temp',
        ),
    ]
