from django.core.management import BaseCommand

from django_gramm.models_manager import UserManager


class Command(BaseCommand):
    help = 'Deletion of all user instances.'

    def handle(self, *args, **options):
        UserManager.delete_all_users()

        self.stdout.write(
            self.style.SUCCESS('Deleting users was successful')
        )
