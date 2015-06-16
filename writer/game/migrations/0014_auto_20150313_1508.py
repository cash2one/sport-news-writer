# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_auto_20150303_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 3, 13, 15, 8, 4, 301334)),
            preserve_default=True,
        ),
    ]
