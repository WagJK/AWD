# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-10 19:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0024_auto_20171111_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 11, 3, 0, 40, 779307)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 11, 3, 0, 40, 779307)),
        ),
    ]
