# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-21 05:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0040_auto_20171121_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 21, 13, 44, 51, 971567)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 21, 13, 44, 51, 969065)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 21, 13, 44, 51, 968065)),
        ),
    ]
