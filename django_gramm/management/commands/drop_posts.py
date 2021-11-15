from django.core.management import BaseCommand

from django_gramm.models_manager import PostManager


class Command(BaseCommand):
    help = 'Deletion of all message instances.'

    def handle(self, *args, **options):
        PostManager.delete_all_posts()

        self.stdout.write(
            self.style.SUCCESS('Deleting the posts was successful')
        )
