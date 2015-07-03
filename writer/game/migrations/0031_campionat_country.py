# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0030_game_used_frases'),
    ]

    operations = [
        migrations.AddField(
            model_name='campionat',
            name='country',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
    ]
