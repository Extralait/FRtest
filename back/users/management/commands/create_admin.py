from django.core.management import BaseCommand

from config import settings
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        for admin in settings.ADMINS:
            User.objects.create_superuser(**admin)
