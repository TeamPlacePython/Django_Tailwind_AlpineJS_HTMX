# Generated by Django 5.1.7 on 2025-03-27 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_carouselimage'),
        ('members', '0002_alter_member_roles_alter_member_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Titre')),
                ('date', models.DateTimeField(verbose_name="Date de l'évènement")),
                ('location', models.TextField(verbose_name='Lieu')),
                ('participants', models.ManyToManyField(related_name='events', to='members.member', verbose_name='Participants')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveIntegerField(blank=True, null=True, verbose_name='Classement')),
                ('score', models.CharField(blank=True, max_length=50, null=True, verbose_name='Score')),
                ('details', models.TextField(blank=True, verbose_name='Détails du résultat')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='home.event', verbose_name='Évènement')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='members.member', verbose_name='Membre')),
            ],
            options={
                'unique_together': {('event', 'member')},
            },
        ),
    ]
