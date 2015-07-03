# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0027_auto_20150623_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=512)),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField()),
                ('game', models.ForeignKey(to='game.Game')),
                ('photo', models.ForeignKey(to='game.Photo', blank=True)),
            ],
        ),
    ]
