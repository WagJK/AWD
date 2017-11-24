# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-24 14:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0059_merge_20171124_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='fee',
            field=models.FloatField(default='0.00'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='generation_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 22, 4, 42, 124931)),
        ),
        migrations.AlterField(
            model_name='message',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 22, 4, 42, 123926)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 22, 4, 42, 122936)),
        ),
        migrations.AlterField(
            model_name='review',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 22, 4, 42, 124931)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 22, 4, 42, 122936)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 22, 4, 42, 122936)),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 22, 4, 42, 123926)),
        ),
    ]
