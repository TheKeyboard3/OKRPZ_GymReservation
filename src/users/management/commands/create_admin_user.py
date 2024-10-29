import os
from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Створити суперкористувача Django зі змінних середовища'

    def handle(self, *args, **options):
        username = os.getenv('SUPERUSER_USERNAME')
        email = os.getenv('SUPERUSER_EMAIL')
        password = os.getenv('SUPERUSER_PASSWORD')

        if not User.objects.filter(username=username).exists():
            admin = User.objects.create_superuser(username, email, password)
            admin.first_name = username.title()
            admin.last_login = admin.date_joined
            admin.save()
            self.stdout.write(self.style.SUCCESS(
                f'Суперкористувач "{username}" успішно створений: '))
        else:
            self.stdout.write(self.style.WARNING(
                f'Суперкористувач "{username}" вже існує'))

    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--super',
            action='store_true',
            default=False,
            help='Створити суперкористувача'
        )
