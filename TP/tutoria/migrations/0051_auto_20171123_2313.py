# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-23 15:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0050_auto_20171123_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='avatar',
            field=models.FileField(default='media/avatars/default.png', upload_to='media/avatars/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='generation_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 23, 23, 13, 23, 124411)),
        ),
        migrations.AlterField(
            model_name='message',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 23, 23, 13, 23, 123410)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 23, 23, 13, 23, 122409)),
        ),
        migrations.AlterField(
            model_name='review',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 23, 23, 13, 23, 124411)),
        ),
        migrations.AlterField(
            model_name='student',
            name='avatar',
            field=models.FileField(default='media/avatars/default.png', upload_to='media/avatars/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 23, 23, 13, 23, 121409)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 23, 23, 13, 23, 121409)),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 23, 23, 13, 23, 123410)),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='avatar',
            field=models.FileField(default='media/avatars/default.png', upload_to='media/avatars/%Y/%m/%d/'),
        ),
    ]
