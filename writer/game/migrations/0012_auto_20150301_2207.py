# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_auto_20150301_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='assist',
            field=models.ForeignKey(related_name='assist_goal', blank=True, to='game.Player', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 3, 1, 22, 7, 35, 666228)),
            preserve_default=True,
        ),
    ]
