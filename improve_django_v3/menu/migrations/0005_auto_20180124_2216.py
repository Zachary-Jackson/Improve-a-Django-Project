# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-01-25 03:16
from __future__ import unicode_literals
from datetime import datetime

from django.db import migrations


def created_date_temp_to_created_date(apps, schema_editor):
    '''This converts the created_date_temp field to created_date.'''
    Item = apps.get_model('menu', 'Item')
    for item in Item.objects.all():
        if item.created_date_temp:
            item.created_date = datetime.date(item.created_date_temp)
            item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_item_created_date'),
    ]

    operations = [
        migrations.RunPython(created_date_temp_to_created_date)
    ]