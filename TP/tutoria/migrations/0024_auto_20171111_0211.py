# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-10 18:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0023_auto_20171110_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='tutor',
            old_name='courses',
            new_name='course',
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 11, 2, 11, 10, 422467)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 11, 2, 11, 10, 422467)),
        ),
        migrations.AddField(
            model_name='tutor',
            name='tag',
            field=models.ManyToManyField(to='tutoria.Tag'),
        ),
    ]
