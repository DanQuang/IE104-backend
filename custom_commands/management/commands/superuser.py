from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
import os
from dotenv import load_dotenv
load_dotenv()

DJANGO_SUPERUSER_NAME = os.getenv('DJANGO_SUPERUSER_NAME')
DJANGO_SUPERUSER_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD')
DJANGO_SUPERUSER_EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL')

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        try:
            User = get_user_model()
            if not User.objects.filter(full_name=DJANGO_SUPERUSER_NAME).exists():
                user = User(
                    email=DJANGO_SUPERUSER_EMAIL,
                    full_name=DJANGO_SUPERUSER_NAME,
                )
                user.set_password(DJANGO_SUPERUSER_PASSWORD)
                user.is_superuser = True                
                user.is_admin = True
                user.save()
                self.stdout.write(self.style.SUCCESS('-----------Successfully created new superuser-----------'))
            else:
                self.stdout.write(self.style.SUCCESS('-----------Superuser already exists-----------'))                
        except Exception as e:
            raise CommandError(e)
        