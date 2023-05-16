# Generated by Django 3.2.16 on 2023-05-09 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='status',
            field=models.IntegerField(choices=[(0, '正常'), (1, '待审核'), (2, '审核未通过')], default=1, verbose_name='状态'),
        ),
    ]
