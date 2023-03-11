# Generated by Django 4.0.4 on 2023-03-11 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s3access', '0014_devices_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapters',
            name='description',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='chapters',
            name='image_url',
            field=models.URLField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='devices',
            name='address',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='devices',
            name='name',
            field=models.TextField(default=None, null=True),
        ),
    ]