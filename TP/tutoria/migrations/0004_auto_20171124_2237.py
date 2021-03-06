# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-24 14:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0003_auto_20171124_2235'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='fee',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='generation_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 22, 37, 33, 28206)),
        ),
        migrations.AlterField(
            model_name='message',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 22, 37, 33, 26171)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 22, 37, 33, 24700)),
        ),
        migrations.AlterField(
            model_name='review',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 22, 37, 33, 27178)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 22, 37, 33, 24195)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 22, 37, 33, 24195)),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 22, 37, 33, 25198)),
        ),
    ]
