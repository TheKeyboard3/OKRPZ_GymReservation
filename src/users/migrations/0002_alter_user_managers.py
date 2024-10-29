# Generated by Django 4.2.11 on 2024-10-18 14:20

import django.contrib.auth.models
from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('clients', users.models.UserClientManager()),
                ('trainers', users.models.UserTrainerManager()),
                ('admins', users.models.UserAdminManager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
