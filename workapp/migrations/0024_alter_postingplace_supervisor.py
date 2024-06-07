# Generated by Django 4.2.13 on 2024-06-06 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0023_alter_studentapplication_year_of_study'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postingplace',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
