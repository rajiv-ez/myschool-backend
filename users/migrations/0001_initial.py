# Generated by Django 5.1.9 on 2025-05-30 16:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academic', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('hr', '0001_initial'),
        ('teaching', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('genre', models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin'), ('A', 'Autre')], max_length=1)),
                ('date_naissance', models.DateField()),
                ('lieu_naissance', models.CharField(max_length=100)),
                ('adresse', models.TextField()),
                ('tel1', models.CharField(max_length=20)),
                ('tel2', models.CharField(blank=True, max_length=20)),
                ('whatsapp', models.CharField(blank=True, max_length=20)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='users/photos/')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_embauche', models.DateField()),
                ('statut', models.CharField(choices=[('ACTIF', 'Actif'), ('CONGE', 'En congé'), ('SUSPENDU', 'Suspendu'), ('INACTIF', 'Inactif')], max_length=20)),
                ('domaines', models.ManyToManyField(blank=True, to='teaching.domaine')),
                ('niveaux', models.ManyToManyField(blank=True, to='academic.niveau')),
                ('poste', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='hr.poste')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tuteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(max_length=100)),
                ('lien_parente', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tuteur', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Eleve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricule', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='eleve', to=settings.AUTH_USER_MODEL)),
                ('tuteurs', models.ManyToManyField(related_name='eleves', to='users.tuteur')),
            ],
        ),
    ]
