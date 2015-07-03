# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0028_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='live',
            field=models.TextField(null=True, blank=True),
        ),
    ]
