# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='events',
        ),
        migrations.AddField(
            model_name='event',
            name='event_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='vendor',
            field=models.ManyToManyField(to='events.Vendor'),
        ),
    ]
