from django.db.models.signals import post_save, post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver

from core.settings.base import MEDIA_ROOT
from main.services import create_image
from .models import User


# @receiver(post_save, sender=User)
# def create_profile(sender, instance: User, created, **kwargs):
#     if created:
#         image_path = f'images/users/{instance.pk}/avatar/{instance.pk}.png'
#         create_image(MEDIA_ROOT / image_path)

#         profile = Profile.objects.create(user=instance)
#         profile.avatar = image_path
#         profile.save()

#     instance.profile.save()


# @receiver(post_migrate)
# def create_default_objects(sender, **kwargs):
#     if not Group.objects.exists():
#         Group.objects.get_or_create(name='Тренери')
