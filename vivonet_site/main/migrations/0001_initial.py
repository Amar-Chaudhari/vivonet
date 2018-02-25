# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-24 23:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Customer_Fname', models.CharField(max_length=60)),
                ('Customer_Lname', models.CharField(max_length=60)),
                ('Customer_Username', models.CharField(max_length=60)),
                ('Customer_Password', models.CharField(max_length=60)),
                ('Customer_Prefix', models.CharField(max_length=60)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Intent_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Intent_Type', models.CharField(max_length=60)),
                ('Source_IP', models.CharField(max_length=60)),
                ('Destination_IP', models.CharField(max_length=60)),
                ('Path', models.CharField(max_length=60)),
                ('timestamp', models.DateTimeField()),
                ('Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Intent_Path_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('switch', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('cookie', models.CharField(max_length=60)),
                ('priority', models.IntegerField()),
                ('active', models.BooleanField()),
                ('ipv4_src', models.CharField(max_length=60)),
                ('ipv4_dst', models.CharField(max_length=60)),
                ('in_port', models.IntegerField()),
                ('actions', models.CharField(max_length=500)),
                ('path_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Intent_Data')),
            ],
        ),
    ]
