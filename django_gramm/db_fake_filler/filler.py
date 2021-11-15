from typing import Union, List, Type
import random
import os

from django.db.models import QuerySet

from django.core.files import File

from django_gramm.models import User
from django_gramm.models_manager import PostManager

from django_gramm.db_fake_filler.fake_data import UserData


class UserFiller:
    def __init__(self, user_model: Type[User] = User):
        self._user_model = user_model

    def fill_and_get_users(
            self, fake_data: UserData
    ) -> Union[QuerySet, List[User]]:
        
        users = []

        for user in fake_data:
            user_object = self._user_model.objects.create(
                username=user.username, email=user.email
            )
            user_object.set_password(raw_password=user.password)
            
            users.append(user_object)

        return users


class PostFillerWithManager:
    def __init__(
            self, path_to_photos: str,
            post_manager: Type[PostManager] = PostManager
    ):

        self._post_manager = post_manager
        self._path_to_photos = path_to_photos

    def _raise_exception_if_photo_dir_not_exists(self) -> None:
        if not os.path.isdir(self._path_to_photos):
            raise ValueError('There is no directory with fake photos!')

    def _raise_exception_if_photo_not_exists(self, photo_number):
        if not os.path.exists(
                f'{self._path_to_photos}/photo_{photo_number}.jpeg'):
            raise ValueError(
                'The name of the photo file '
                'must match the pattern - "photo_i.jpeg".'
            )

    def _create_fake_post(self, user: User, photo_number) -> None:
        self._raise_exception_if_photo_not_exists(photo_number)

        with open(
                f'{self._path_to_photos}/photo_{photo_number}.jpeg', 'rb'
        ) as photo:

            django_photo = File(photo)

            PostManager.create_new_post(
                user=user, post_image=django_photo,
                description=f'{photo_number} Test decsription'
            )

    def fill_posts(self, fake_users: Union[QuerySet, List[User]]) -> None:
        self._raise_exception_if_photo_dir_not_exists()

        for user in fake_users:
            for photo_num in range(1, random.randint(1, 17)):
                self._create_fake_post(user, photo_num)


class DbFiller:
    def __init__(
            self, user_filler: UserFiller,
            post_filler: PostFillerWithManager
    ):
        self._user_filler = user_filler
        self._post_filler = post_filler

    def fill_db(self, fake_users: UserData):
        users = self._user_filler.fill_and_get_users(fake_users)

        self._post_filler.fill_posts(users)
