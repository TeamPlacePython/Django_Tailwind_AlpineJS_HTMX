# Generated by Django 5.1.7 on 2025-04-24 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='orientation',
            field=models.CharField(blank=True, choices=[('landscape', 'Landscape'), ('portrait', 'Portrait'), ('square', 'Square')], editable=False, max_length=10, null=True),
        ),
    ]
