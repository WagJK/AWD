# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-01 04:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0010_auto_20171101_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 1, 12, 2, 25, 614497)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 1, 12, 2, 25, 614497)),
        ),
    ]
