# Generated by Django 5.1.7 on 2025-05-05 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_remove_image_description_remove_image_orientation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Image',
        ),
    ]
