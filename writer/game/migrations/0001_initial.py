# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campionat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('url', models.CharField(max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conclusion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(null=True, blank=True)),
                ('urcare', models.BooleanField(default=False)),
                ('coborire', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FirstGoalFrase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(null=True, blank=True)),
                ('min_minute', models.IntegerField(null=True, blank=True)),
                ('max_minute', models.IntegerField(null=True, blank=True)),
                ('only', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('goal_team1', models.IntegerField(default=0)),
                ('goal_team2', models.IntegerField(default=0)),
                ('pub_date', models.DateField(default=datetime.datetime(2015, 2, 27, 10, 58, 7, 361746))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minute', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LastGoalFrase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(null=True, blank=True)),
                ('equal', models.BooleanField(default=False)),
                ('reverse', models.BooleanField(default=False)),
                ('only', models.BooleanField(default=False)),
                ('victory', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('goals_in_season', models.IntegerField(default=0)),
                ('goals_total', models.IntegerField(default=0)),
                ('nationality', models.CharField(max_length=128, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegularGoalFrase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(null=True, blank=True)),
                ('equal', models.BooleanField(default=False)),
                ('reverse', models.BooleanField(default=False)),
                ('only', models.BooleanField(default=False)),
                ('duble', models.BooleanField(default=False)),
                ('triple', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Synonims',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('syns', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=128, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TitleFrase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(null=True, blank=True)),
                ('min_score_diference', models.IntegerField(null=True, blank=True)),
                ('max_score_diference', models.IntegerField(null=True, blank=True)),
                ('min_total_goals', models.IntegerField(null=True, blank=True)),
                ('max_total_goals', models.IntegerField(null=True, blank=True)),
                ('last_goal_final', models.BooleanField(default=False)),
                ('triple', models.BooleanField(default=False)),
                ('duble', models.BooleanField(default=False)),
                ('urcare', models.BooleanField(default=False)),
                ('coborire', models.BooleanField(default=False)),
                ('win_ser', models.BooleanField(default=False)),
                ('stop_win_ser', models.BooleanField(default=False)),
                ('lose_ser', models.BooleanField(default=False)),
                ('stop_lose_ser', models.BooleanField(default=False)),
                ('nonlose_ser', models.BooleanField(default=False)),
                ('stop_nonlose_ser', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='goal',
            name='author',
            field=models.ForeignKey(blank=True, to='game.Player', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goal',
            name='team',
            field=models.ForeignKey(to='game.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='goals',
            field=models.ManyToManyField(to='game.Goal', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='team1',
            field=models.ForeignKey(related_name='game_team1', to='game.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='team2',
            field=models.ForeignKey(related_name='game_team2', to='game.Team'),
            preserve_default=True,
        ),
    ]
