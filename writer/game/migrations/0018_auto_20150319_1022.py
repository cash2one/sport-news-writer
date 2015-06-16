# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_auto_20150316_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='campionat',
            field=models.ForeignKey(default=1, to='game.Campionat'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 3, 19, 10, 21, 49, 685157)),
            preserve_default=True,
        ),
    ]
