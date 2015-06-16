# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='campionat',
            field=models.ForeignKey(blank=True, to='game.Campionat', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 2, 27, 10, 58, 36, 562177)),
            preserve_default=True,
        ),
    ]
