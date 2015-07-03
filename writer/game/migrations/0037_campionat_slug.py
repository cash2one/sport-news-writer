# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0036_news_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='campionat',
            name='slug',
            field=models.CharField(default='', max_length=160),
            preserve_default=False,
        ),
    ]
