# Generated by Django 4.2.13 on 2024-06-12 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0030_rename_username_or_matric_or_staff_id_user_username_or_staff_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username_or_staff_id',
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, default='new_user', max_length=20, null=True),
        ),
    ]