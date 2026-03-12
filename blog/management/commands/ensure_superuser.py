import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser from env vars if it does not already exist."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "DJANGO_SUPERUSER_USERNAME/DJANGO_SUPERUSER_PASSWORD not set; skipping superuser creation."
                )
            )
            return

        User = get_user_model()

        existing_user = User.objects.filter(username=username).first()
        if existing_user is not None:
            existing_user.is_staff = True
            existing_user.is_superuser = True
            if email:
                existing_user.email = email
            existing_user.set_password(password)
            existing_user.save()
            self.stdout.write(self.style.SUCCESS(f"Updated superuser password/flags: {username}"))
            return

        user = User.objects.create_superuser(
            username=username,
            email=email or "",
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Created superuser: {username}"))
