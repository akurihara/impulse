# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-03 04:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0004_auto_20170201_0605'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitorStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, b'Created'), (1, b'Activated'), (2, b'Deactivated')])),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('monitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='alert.Monitor')),
            ],
            options={
                'get_latest_by': 'id',
            },
        ),
    ]