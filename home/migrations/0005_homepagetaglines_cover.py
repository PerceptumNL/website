# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-25 15:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0012_copy_image_permissions_to_collections'),
        ('home', '0004_homepagetaglines'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagetaglines',
            name='cover',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]