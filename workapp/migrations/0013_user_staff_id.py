# Generated by Django 4.2.13 on 2024-05-30 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0012_studentapplication_year_of_study'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='staff_id',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]