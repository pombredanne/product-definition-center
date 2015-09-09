# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
        ('component', '0007_auto_20150821_0834'),
    ]

    operations = [
        migrations.CreateModel(
            name='GCContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='RCContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='globalcomponent',
            name='contacts',
        ),
        migrations.RemoveField(
            model_name='releasecomponent',
            name='contacts',
        ),
        migrations.AddField(
            model_name='rccontact',
            name='component',
            field=models.ForeignKey(to='component.ReleaseComponent'),
        ),
        migrations.AddField(
            model_name='rccontact',
            name='contact',
            field=models.ForeignKey(to='contact.Contact', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='rccontact',
            name='contact_role',
            field=models.ForeignKey(to='contact.ContactRole', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='gccontact',
            name='component',
            field=models.ForeignKey(to='component.GlobalComponent'),
        ),
        migrations.AddField(
            model_name='gccontact',
            name='contact',
            field=models.ForeignKey(to='contact.Contact', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='gccontact',
            name='contact_role',
            field=models.ForeignKey(to='contact.ContactRole', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterUniqueTogether(
            name='rccontact',
            unique_together=set([('contact_role', 'contact', 'component')]),
        ),
        migrations.AlterUniqueTogether(
            name='gccontact',
            unique_together=set([('contact_role', 'contact', 'component')]),
        ),
    ]
