# Generated by Django 4.2.13 on 2024-05-29 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0010_user_contact_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, default='08012345678', max_length=12, null=True),
        ),
    ]