# Generated by Django 4.2.13 on 2024-05-30 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0011_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentapplication',
            name='year_of_study',
            field=models.IntegerField(blank=True, default=2024, null=True),
        ),
    ]
