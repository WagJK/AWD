# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-10 13:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0025_auto_20171110_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 10, 21, 31, 27, 780145)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 10, 21, 31, 27, 780145)),
        ),
    ]