import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update the superuser from DJANGO_SUPERUSER_* env vars (always syncs password)."

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email    = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@eduimperium.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")

        if not password:
            self.stdout.write(
                self.style.WARNING(
                    "DJANGO_SUPERUSER_PASSWORD not set — skipping superuser creation."
                )
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )

        # Always sync the password so env-var changes take effect on redeploy
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.email = email
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Superuser '{username}' created."))
        else:
            self.stdout.write(self.style.SUCCESS(f"✅ Superuser '{username}' password updated."))
