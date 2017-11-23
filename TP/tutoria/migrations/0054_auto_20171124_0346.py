# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-23 19:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0053_auto_20171124_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='generation_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 3, 46, 34, 751886)),
        ),
        migrations.AlterField(
            model_name='message',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 3, 46, 34, 750885)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 3, 46, 34, 749884)),
        ),
        migrations.AlterField(
            model_name='review',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 3, 46, 34, 751886)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 3, 46, 34, 749884)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 3, 46, 34, 749884)),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 3, 46, 34, 750885)),
        ),
    ]
