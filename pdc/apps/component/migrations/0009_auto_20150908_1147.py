# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20150908_1147'),
        ('component', '0008_auto_20150908_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalcomponent',
            name='contacts',
            field=models.ManyToManyField(to='contact.Contact', through='component.GCContact'),
        ),
        migrations.AddField(
            model_name='releasecomponent',
            name='contacts',
            field=models.ManyToManyField(to='contact.Contact', through='component.RCContact'),
        ),
    ]
