# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0049_projectstatus_plural'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectstatus',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
