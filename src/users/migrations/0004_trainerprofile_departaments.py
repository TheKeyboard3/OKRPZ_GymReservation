# Generated by Django 4.2.11 on 2024-10-30 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_alter_workschedule_trainer'),
        ('users', '0003_alter_user_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainerprofile',
            name='departaments',
            field=models.ManyToManyField(blank=True, to='booking.departament', verbose_name='Відділення у яких працює тренер'),
        ),
    ]
