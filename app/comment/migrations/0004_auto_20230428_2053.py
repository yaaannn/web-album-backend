# Generated by Django 3.2.16 on 2023-04-28 20:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import extension.custom_field_ext


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_table'),
        ('comment', '0003_alter_comment_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=255, verbose_name='评论内容'),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', extension.custom_field_ext.TimestampField(blank=True, editable=False, help_text='创建时间戳', validators=[django.core.validators.MinValueValidator(limit_value=0)], verbose_name='创建时间戳')),
                ('update_time', extension.custom_field_ext.TimestampField(blank=True, editable=False, help_text='更新时间戳', validators=[django.core.validators.MinValueValidator(limit_value=0)], verbose_name='更新时间戳')),
                ('content', models.CharField(max_length=255, verbose_name='回复内容')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user', verbose_name='作者')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comment.comment', verbose_name='评论')),
            ],
            options={
                'verbose_name': '回复表',
                'verbose_name_plural': '回复表',
                'db_table': 'a_reply',
            },
        ),
    ]
