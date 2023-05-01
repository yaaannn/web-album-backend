# Generated by Django 3.2.16 on 2023-04-20 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0003_alter_photo_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='status',
        ),
        migrations.AddField(
            model_name='photo',
            name='is_public',
            field=models.BooleanField(default=True, verbose_name='是否公开'),
        ),
    ]
