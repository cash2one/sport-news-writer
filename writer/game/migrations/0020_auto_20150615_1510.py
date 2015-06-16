# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0019_auto_20150615_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='photo',
            field=models.ManyToManyField(to='game.Photo'),
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 6, 15, 15, 10, 37, 465735)),
        ),
    ]
