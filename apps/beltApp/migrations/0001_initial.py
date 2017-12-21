# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-21 22:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('alias', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('bday', models.DateField(default='2000-01-01')),
                ('friends', models.ManyToManyField(related_name='_user_friends_+', to='beltApp.User')),
            ],
        ),
    ]
