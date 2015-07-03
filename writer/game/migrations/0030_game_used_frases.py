# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0029_game_live'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='used_frases',
            field=models.TextField(default=b'{"title": None, "begin": None, "first": None, "group": [], "regular": [], "last": None, "conclusion": None}'),
        ),
    ]
