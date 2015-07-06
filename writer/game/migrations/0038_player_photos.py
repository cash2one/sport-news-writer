# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0037_campionat_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='photos',
            field=models.ManyToManyField(to='game.Photo', null=True, blank=True),
        ),
    ]
