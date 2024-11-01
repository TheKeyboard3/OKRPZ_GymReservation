# Generated by Django 4.2.11 on 2024-10-18 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_managers'),
        ('booking', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workschedule',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_schedules', to='users.trainerprofile', verbose_name='Тренер'),
        ),
    ]
