# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 12:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpage_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BlogIndexRelatedLink',
            new_name='BlogRelatedLink',
        ),
    ]
