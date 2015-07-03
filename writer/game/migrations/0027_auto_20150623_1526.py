# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0026_goalgroupfrase'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='images',
            field=models.ManyToManyField(to='game.Photo', blank=True),
        ),
        migrations.AddField(
            model_name='game',
            name='video',
            field=models.TextField(null=True, blank=True),
        ),
    ]
