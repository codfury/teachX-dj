# Generated by Django 4.0.4 on 2023-02-05 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s3access', '0002_alter_chapters_options_alter_classes_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapters',
            name='description',
            field=models.TextField(blank=True, default=None),
        ),
    ]
