# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-16 03:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_credit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credit',
            name='user',
        ),
        migrations.DeleteModel(
            name='Credit',
        ),
    ]
