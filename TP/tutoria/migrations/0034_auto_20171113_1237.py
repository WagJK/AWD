# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-13 04:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0033_auto_20171112_2222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timeslot',
            old_name='available_for_booking',
            new_name='bookable',
        ),
        migrations.RenameField(
            model_name='timeslot',
            old_name='available_for_cancelling',
            new_name='cancellable',
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 13, 12, 37, 29, 534441)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 13, 12, 37, 29, 534441)),
        ),
    ]