from django.db.models.signals import post_migrate
from django.contrib.sites.models import Site
from django.dispatch import receiver
from django.conf import settings


@receiver(post_migrate)
def create_default_objects(sender, **kwargs) -> None:
    if not Site.objects.filter(domain=settings.DOMAIN).exists():
        for site in Site.objects.all():
            site.delete()

        Site.objects.create(
            id=settings.SITE_ID,
            domain=settings.DOMAIN,
            name=settings.APP_NAME)
