# Generated by Django 5.1.6 on 2025-02-14 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_staff',
        ),
    ]
