# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-01-25 18:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0008_auto_20180125_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='expiration_date',
            field=models.DateField(default=datetime.date(2018, 1, 25)),
            preserve_default=False,
        ),
    ]
