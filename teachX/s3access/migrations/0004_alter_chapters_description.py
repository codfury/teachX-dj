# Generated by Django 4.0.4 on 2023-02-05 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s3access', '0003_alter_chapters_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapters',
            name='description',
            field=models.TextField(default='Chapter Desc'),
        ),
    ]
