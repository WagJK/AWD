# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-22 06:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0002_auto_20171022_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='endTime',
            field=models.TextField(default='1:00a.m'),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='startTime',
            field=models.TextField(default='0:00a.m'),
        ),
        migrations.AlterField(
            model_name='tutorprofile',
            name='availability',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tutorprofile',
            name='average_review',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='tutorprofile',
            name='contact',
            field=models.EmailField(default='tutor@hku.hk', max_length=254),
        ),
        migrations.AlterField(
            model_name='tutorprofile',
            name='hourly_rate',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='tutorprofile',
            name='university',
            field=models.CharField(default='HKU', max_length=50),
        ),
    ]
