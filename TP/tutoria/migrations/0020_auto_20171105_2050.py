# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-05 12:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0019_auto_20171105_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 5, 20, 50, 27, 992201)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 5, 20, 50, 27, 992201)),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='profile',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='tutoria.TutorProfile'),
        ),
    ]
