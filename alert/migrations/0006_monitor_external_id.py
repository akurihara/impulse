# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-13 05:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0005_monitorstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitor',
            name='external_id',
            field=models.CharField(default='test', max_length=10),
            preserve_default=False,
        ),
    ]
