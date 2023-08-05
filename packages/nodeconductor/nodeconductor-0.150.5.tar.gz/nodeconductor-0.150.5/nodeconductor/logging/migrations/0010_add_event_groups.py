# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import nodeconductor.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('logging', '0009_add_device_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailhook',
            name='event_groups',
            field=nodeconductor.core.fields.JSONField(default=[], verbose_name='List of event groups'),
        ),
        migrations.AddField(
            model_name='pushhook',
            name='event_groups',
            field=nodeconductor.core.fields.JSONField(default=[], verbose_name='List of event groups'),
        ),
        migrations.AddField(
            model_name='systemnotification',
            name='event_groups',
            field=nodeconductor.core.fields.JSONField(default=[], verbose_name='List of event groups'),
        ),
        migrations.AddField(
            model_name='webhook',
            name='event_groups',
            field=nodeconductor.core.fields.JSONField(default=[], verbose_name='List of event groups'),
        ),
    ]
