# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0020_auto_20150615_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='recipient',
            field=models.ForeignKey(related_name='recipient_team', blank=True, to='game.Team', null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 6, 16, 10, 20, 30, 451583)),
        ),
    ]
