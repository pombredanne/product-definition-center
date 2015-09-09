# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0008_auto_20150908_1147'),
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rolecontact',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='rolecontact',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='rolecontact',
            name='contact_role',
        ),
        migrations.DeleteModel(
            name='RoleContact',
        ),
    ]
