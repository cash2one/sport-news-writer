# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0033_auto_20150630_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Couch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('photo', models.ManyToManyField(to='game.Photo', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='couch_human',
            field=models.ForeignKey(blank=True, to='game.Couch', null=True),
        ),
    ]
