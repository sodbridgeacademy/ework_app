# Generated by Django 4.2.13 on 2024-05-30 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0013_user_staff_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='staff_id',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
