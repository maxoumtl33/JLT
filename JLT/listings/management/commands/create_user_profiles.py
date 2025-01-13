from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import UserProfile  # Make sure to import your actual model here

class Command(BaseCommand):
    help = 'Create UserProfile objects for all existing users'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                self.stdout.write(f"Created profile for user: {user.username}")
            else:
                self.stdout.write(f"Profile already exists for user: {user.username}")
