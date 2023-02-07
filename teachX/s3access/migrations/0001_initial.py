# Generated by Django 4.0.4 on 2023-02-05 13:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Class', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='devices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.TextField(unique=True)),
                ('name', models.TextField()),
                ('address', models.TextField()),
                ('updated_at', models.DateTimeField(default=datetime.datetime.utcnow)),
            ],
        ),
        migrations.CreateModel(
            name='subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='chapters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.TextField()),
                ('s3object_value', models.TextField()),
                ('updated_at', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('Class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='s3access.classes')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='s3access.subjects')),
            ],
        ),
    ]
