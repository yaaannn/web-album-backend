# Generated by Django 3.2.16 on 2023-01-28 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(blank=True, default='1970-01-01', verbose_name='生日'),
        ),
    ]
