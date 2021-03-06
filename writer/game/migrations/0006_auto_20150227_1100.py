# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20150227_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='author',
            field=models.ForeignKey(blank=True, to='game.Player', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 2, 27, 11, 0, 49, 891377)),
            preserve_default=True,
        ),
    ]
