# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20151021_0209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='vendor',
        ),
        migrations.AddField(
            model_name='vendor',
            name='events',
            field=models.ManyToManyField(to='events.Event'),
        ),
    ]
