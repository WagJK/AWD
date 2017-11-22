# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-22 09:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0044_auto_20171122_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 22, 17, 11, 22, 92709)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 22, 17, 11, 22, 91708)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 22, 17, 11, 22, 90707)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 22, 17, 11, 22, 90707)),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 22, 17, 11, 22, 91708)),
        ),
    ]