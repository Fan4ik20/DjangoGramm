from django.core.management import BaseCommand
from django.db.utils import IntegrityError

from django_gramm.db_fake_filler.filler import (
    PostFillerWithManager,
    DbFiller, UserFiller
)

from django_gramm.db_fake_filler.fake_data import fake_users, UserData
from django_gramm.models_manager import UserManager


class Command(BaseCommand):
    help = 'Filling the db with fake users and posts.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-p', '--path_to_photos', type=str,
            help='Changes the default photo path to yours.'
        )

    @staticmethod
    def _fill_db(path_to_photos, fake_users_data: UserData):
        user_filler = UserFiller()
        post_filler = PostFillerWithManager(path_to_photos)

        db_filler = DbFiller(user_filler, post_filler)

        db_filler.fill_db(fake_users_data)

    @staticmethod
    def _flush_users_and_posts():
        UserManager.delete_all_users()

    def handle(self, *args, **kwargs):
        path_to_photos = (
            'django_gramm/db_fake_filler/fake_photos'
            if not (path_to_photos_ := kwargs['path_to_photos'])
            else path_to_photos_
        )

        try:
            self._fill_db(path_to_photos, fake_users)
        except (IntegrityError, ValueError) as exception:
            self.stdout.write(
                self.style.ERROR(
                    exception
                )
            )

            self.stdout.write(
                self.style.ERROR(
                    'Error filling db - flushing Posts and Users tables'
                )
            )

            self._flush_users_and_posts()

        else:
            self.stdout.write(self.style.SUCCESS(
                'Filling of the database was successful'
            ))
