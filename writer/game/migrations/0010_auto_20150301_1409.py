# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_auto_20150227_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='penalty',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 3, 1, 14, 9, 3, 323453)),
            preserve_default=True,
        ),
    ]
