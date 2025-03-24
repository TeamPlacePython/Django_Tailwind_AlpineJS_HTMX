# Generated by Django 5.1.7 on 2025-03-24 10:14

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sport', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=100, verbose_name='Last Name')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Birth Date')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be in format: '+999999999'.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone Number')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address')),
                ('address_complement', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address complement')),
                ('postal_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Postal Code')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='City')),
                ('roles', models.CharField(blank=True, choices=[('coach', "Maître d'armes"), ('member', 'Membre'), ('president', 'Président'), ('treasurer', 'Trésorier'), ('vice-president', 'Vice-Président'), ('secretary', 'Secrétaire'), ('web-master', 'Web-master'), ('visitor', 'Visiteur'), ('testman', 'Testman')], default='visitor', max_length=20, verbose_name='Role')),
                ('status', models.CharField(choices=[('active', 'Actif'), ('inactive', 'Inactif'), ('pending', 'En attente')], default='pending', max_length=10, verbose_name='Status')),
                ('weapon', models.CharField(blank=True, choices=[('epee', 'Épée'), ('fleuret', 'Fleuret'), ('sabre', 'Sabre')], max_length=10, null=True, verbose_name='weapon')),
                ('gender', models.CharField(blank=True, choices=[('male', 'Homme'), ('female', 'Femme'), ('other', 'Autre')], max_length=10, null=True, verbose_name='gender')),
                ('handeness', models.CharField(blank=True, choices=[('right', 'Droitier'), ('left', 'Gaucher'), ('ambidextrous', 'Ambidextre')], max_length=15, null=True, verbose_name='handeness')),
                ('date_joined', models.DateField(auto_now_add=True, verbose_name='Date Joined')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='member_photos/', verbose_name='Photo')),
                ('sports_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sport.sportscategory', verbose_name='Sports Category')),
                ('tags', models.ManyToManyField(blank=True, related_name='members', to='members.tag', verbose_name='tag')),
            ],
            options={
                'verbose_name': 'Member',
                'verbose_name_plural': 'Members',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='MembershipFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=False, verbose_name='Valid Payment')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fees', to='members.member')),
                ('sports_category', models.ForeignKey(blank=True, help_text='Catégorie associée à ce paiement', null=True, on_delete=django.db.models.deletion.SET_NULL, to='sport.sportscategory', verbose_name='Category')),
            ],
            options={
                'ordering': ['member'],
            },
        ),
    ]
