# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-26 03:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_auto_20170426_0355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='country',
            field=models.CharField(max_length=255),
        ),
    ]
