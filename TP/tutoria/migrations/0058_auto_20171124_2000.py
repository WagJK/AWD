# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-24 12:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0057_auto_20171124_1640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='fee',
        ),
        migrations.AlterField(
            model_name='coupon',
            name='generation_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 20, 0, 16, 613557)),
        ),
        migrations.AlterField(
            model_name='message',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 20, 0, 16, 612054)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 20, 0, 16, 611551)),
        ),
        migrations.AlterField(
            model_name='review',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 20, 0, 16, 612555)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 20, 0, 16, 611053)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 20, 0, 16, 611053)),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 24, 20, 0, 16, 611551)),
        ),
    ]
