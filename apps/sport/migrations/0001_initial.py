# Generated by Django 5.1.7 on 2025-04-02 08:01

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SportsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_year', models.IntegerField(blank=True, null=True)),
                ('end_year', models.IntegerField(blank=True, null=True)),
                ('fee_amount', models.DecimalField(blank=True, decimal_places=2, help_text='Montant de la cotisation pour cette catégorie', max_digits=6, null=True, verbose_name='Membership Fee (€)')),
                ('monday_hours', models.CharField(blank=True, max_length=50, null=True)),
                ('tuesday_hours', models.CharField(blank=True, max_length=50, null=True)),
                ('wednesday_hours', models.CharField(blank=True, max_length=50, null=True)),
                ('thursday_hours', models.CharField(blank=True, max_length=50, null=True)),
                ('friday_hours', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Sports categories',
                'ordering': ['-start_year'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Titre')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name="Date de l'évènement")),
                ('location', models.TextField(verbose_name='Lieu')),
                ('participants', models.ManyToManyField(related_name='events', to='members.member', verbose_name='Participants')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Titre de la performance')),
                ('description', models.TextField(verbose_name='Détails de la performance')),
                ('creation_date', models.DateField(verbose_name='Date de réalisation')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performances', to='members.member')),
            ],
            options={
                'verbose_name': 'Performance',
                'verbose_name_plural': 'Performances',
                'ordering': ['-creation_date'],
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveIntegerField(blank=True, null=True, verbose_name='Classement')),
                ('information', models.CharField(blank=True, max_length=50, null=True, verbose_name='Information')),
                ('details', models.TextField(blank=True, verbose_name='Détails du résultat')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='sport.event', verbose_name='Évènement')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='members.member', verbose_name='Membre')),
            ],
            options={
                'ordering': ['rank'],
                'constraints': [models.UniqueConstraint(fields=('event', 'member'), name='unique_event_member')],
            },
        ),
    ]
