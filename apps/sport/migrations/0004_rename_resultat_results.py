# Generated by Django 5.1.7 on 2025-03-25 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_alter_member_roles_alter_member_status'),
        ('sport', '0003_alter_sportscategory_options_performance_resultat'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Resultat',
            new_name='Results',
        ),
    ]
