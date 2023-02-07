# Generated by Django 4.0.4 on 2023-02-07 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s3access', '0008_alter_classes_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapters',
            options={'ordering': ['chapter_number'], 'verbose_name_plural': 'chapters'},
        ),
        migrations.AlterModelOptions(
            name='subjects',
            options={'ordering': ['subject'], 'verbose_name_plural': 'subjects'},
        ),
        migrations.AddField(
            model_name='chapters',
            name='chapter_number',
            field=models.IntegerField(default=1),
        ),
    ]