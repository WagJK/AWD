# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-14 15:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0035_auto_20171113_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='mytutor',
            name='commission_rate',
            field=models.FloatField(default='0.05'),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='within_week',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 14, 23, 33, 58, 597931)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 14, 23, 33, 58, 597931)),
        ),
    ]