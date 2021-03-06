# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-24 22:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_verified', models.BooleanField(default=False, help_text='Designates whether this user has completed the email verification process to allow login.', verbose_name='verified')),
                ('user_type', models.CharField(choices=[(b'S', b'swimmer'), (b'R', b'runner')], default=b'S', max_length=2)),
                ('date_of_birth', models.DateField(null=True)),
                ('city_id', models.IntegerField(blank=True, help_text='??', null=True, verbose_name='??')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('surname', models.CharField(blank=True, max_length=100, null=True)),
                ('bio', models.CharField(blank=True, max_length=500, null=True)),
                ('avatar', models.CharField(blank=True, max_length=100, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Runner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(blank=True, help_text='Ranking position.', null=True, verbose_name='Ranking position.')),
                ('meters', models.IntegerField(blank=True, default=0, help_text='Total meters.', verbose_name='Total meters.')),
                ('minutes', models.IntegerField(blank=True, default=0, help_text='Total minutes.', verbose_name='Total minutes.')),
                ('trend', models.CharField(choices=[(b'up', b'UP'), (b'down', b'DOWN')], default=b'down', max_length=10)),
                ('type', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Swimmer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(blank=True, help_text='Ranking position.', null=True, verbose_name='Ranking position.')),
                ('meters', models.IntegerField(blank=True, default=0, help_text='Total meters.', verbose_name='Total meters.')),
                ('minutes', models.IntegerField(blank=True, default=0, help_text='Total minutes.', verbose_name='Total minutes.')),
                ('strokes', models.IntegerField(blank=True, default=0, help_text='Total strokes', verbose_name='Total strokes.')),
                ('metersAverage', models.IntegerField(blank=True, default=0, help_text='Meters average.', verbose_name='Meters average.')),
                ('minutesAverage', models.IntegerField(blank=True, default=0, help_text='Minutes average', verbose_name='Minutes average.')),
                ('trend', models.CharField(choices=[(b'up', b'UP'), (b'down', b'DOWN')], default=b'down', max_length=10)),
                ('type', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
