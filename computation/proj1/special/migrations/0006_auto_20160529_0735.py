# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-29 07:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('special', '0005_auto_20160529_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='ticker_symbol',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
