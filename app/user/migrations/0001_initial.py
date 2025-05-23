# Generated by Django 3.2.16 on 2023-05-03 17:38

import django.core.validators
from django.db import migrations, models
import extension.custom_field_ext


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', extension.custom_field_ext.TimestampField(blank=True, editable=False, help_text='创建时间戳', validators=[django.core.validators.MinValueValidator(limit_value=0)], verbose_name='创建时间戳')),
                ('update_time', extension.custom_field_ext.TimestampField(blank=True, editable=False, help_text='更新时间戳', validators=[django.core.validators.MinValueValidator(limit_value=0)], verbose_name='更新时间戳')),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=255, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('mobile', models.CharField(blank=True, default='', max_length=11, verbose_name='手机号')),
                ('nickname', models.CharField(blank=True, default='', max_length=32, verbose_name='昵称')),
                ('regions', models.CharField(blank=True, default='', max_length=255, verbose_name='地区')),
                ('avatar', models.CharField(blank=True, default='', max_length=255, verbose_name='头像')),
                ('birthday', models.DateField(blank=True, default='1970-01-01', verbose_name='生日')),
                ('cover', models.CharField(blank=True, default='', max_length=255, verbose_name='封面')),
                ('gender', models.CharField(choices=[('0', '男'), ('1', '女'), ('2', '秘密')], max_length=1, verbose_name='性别')),
                ('is_freeze', models.BooleanField(default=False, verbose_name='是否冻结')),
                ('jwt_version', models.IntegerField(default=0, verbose_name='jwt版本')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
                'db_table': 'a_user',
            },
        ),
    ]
