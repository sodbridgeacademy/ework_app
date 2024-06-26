# Generated by Django 4.2.13 on 2024-06-12 08:57

import datetime
import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0028_rename_supervisor_checked_workstatus_supervisor_approval_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username_or_matric_or_staff_id',
            field=models.CharField(blank=True, default='new_user', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default=datetime.datetime(2024, 6, 12, 8, 57, 2, 419658, tzinfo=datetime.timezone.utc), error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='workstatus',
            name='comments',
            field=models.TextField(null=True),
        ),
    ]
