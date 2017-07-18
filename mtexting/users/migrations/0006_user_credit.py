# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-18 16:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0002_remove_credit_user'),
        ('users', '0005_auto_20170716_0318'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='credit',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='plan.Credit'),
        ),
    ]
