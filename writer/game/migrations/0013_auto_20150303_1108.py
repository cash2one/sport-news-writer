# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_auto_20150301_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='lider',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='loser',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 3, 3, 11, 8, 11, 345625)),
            preserve_default=True,
        ),
    ]
