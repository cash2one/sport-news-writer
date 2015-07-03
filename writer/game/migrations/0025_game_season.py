# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import writer.game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0024_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='season',
            field=models.ForeignKey(default=writer.game.models.get_season, to='game.Season'),
        ),
    ]
