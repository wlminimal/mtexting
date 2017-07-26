# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 22:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0005_auto_20170726_2246'),
        ('users', '0008_auto_20170718_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to='plan.Plan'),
        ),
    ]