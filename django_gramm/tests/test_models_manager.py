import os

from django.core.files import File
from django.test import TestCase

from django_gramm.models_manager import (
    PostManager, UserManager, CommentManager
)

from django_gramm.tests.factories import (
    UserFactory, PostFactory
)

from django_gramm import models


class TestPostManager(TestCase):
    def setUp(self) -> None:
        self._test_users = [UserFactory() for _ in range(10)]

    def tearDown(self) -> None:
        PostManager.delete_all_posts()
        UserManager.delete_all_users()

    @staticmethod
    def _check_if_test_photo_exists(file_path: str) -> None:
        if not os.path.exists(file_path):
            raise ValueError(f'There is no file under the path - {file_path}')

    def test_create_new_post(self):
        _file_path = 'django_gramm/tests/test_files/test_photo.jpeg'

        self._check_if_test_photo_exists(_file_path)

        with open(_file_path, 'rb') as test_image:
            django_photo = File(test_image)

            for user in self._test_users:
                new_post = PostManager.create_new_post(
                    user, django_photo, 'Test Description'
                )
                post_from_db = models.Post.objects.get(pk=new_post.pk)

                with self.subTest():
                    self.assertEqual(new_post, post_from_db)
                    self.assertIn(new_post, models.Post.objects.all())

    def test_get_posts_with_annotated_data_on_having_additional_attr(self):
        posts = PostManager.get_posts_with_annotated_data()

        for post in posts:
            with self.subTest():
                self.assertTrue(hasattr(post, 'likes_count'))
                self.assertTrue(hasattr(post, 'comments_count'))

    def _create_test_user_posts_dict(self) -> dict:
        user_posts = {}
        for user in self._test_users:
            if user not in user_posts:
                user_posts[user] = []

            for _ in range(5):
                user_posts[user].append(PostFactory(user=user))

        return user_posts

    def test_get_posts_with_related_data_by_user(self):
        test_user_posts = self._create_test_user_posts_dict()

        for test_user, test_posts in test_user_posts.items():
            posts_from_manager = (
                PostManager.get_posts_with_related_data_by_user(user=test_user)
            )

            for test_post in test_posts:
                with self.subTest():
                    self.assertIn(test_post, posts_from_manager)

    def test_get_recommended_posts_users_posts_not_in_queryset(self):
        test_user_posts = self._create_test_user_posts_dict()

        for user, posts in test_user_posts.items():
            recommended_posts = PostManager.get_recommended_posts(user=user)

            for user_post in posts:
                with self.subTest():
                    self.assertNotIn(user_post, recommended_posts)

    def _create_posts_structure_with_likes_dict_right_ordering(self) -> dict:
        # {likes_count : (post)(liked_user)}

        ordering_users_liked_post = {
            (3, 1, 2): (
                (
                    self._test_users[0],
                    self._test_users[1],
                    self._test_users[2]
                ),

                (self._test_users[3],),
                (self._test_users[5], self._test_users[6])
            ),

            (5, 2, 1, 4, 3): (
                (
                    self._test_users[0], self._test_users[1],
                    self._test_users[2],
                    self._test_users[3], self._test_users[4]
                ),

                (self._test_users[5], self._test_users[6]),
                (self._test_users[7],),

                (
                    self._test_users[8], self._test_users[9],
                    self._test_users[0],
                    self._test_users[1],
                ),

                (self._test_users[2], self._test_users[3], self._test_users[1])
            ),
            (3, 2, 1, 4): (
                (
                    self._test_users[0], self._test_users[2],
                    self._test_users[3]
                ),

                (self._test_users[2], self._test_users[4]),
                (self._test_users[3],),

                (
                    self._test_users[5], self._test_users[6],
                    self._test_users[2],
                    self._test_users[1]
                )
            )
        }

        return ordering_users_liked_post

    @staticmethod
    def _create_posts_with_likes(liked_users: list) -> list:
        posts = [
            PostFactory.create(likes=users) for users in liked_users
        ]

        return posts

    def test_get_recommended_post_ordering_by_likes(self):
        user = self._test_users[0]

        ordering_users_liked_post = (
            self._create_posts_structure_with_likes_dict_right_ordering()
        )

        for ordering, liked_users in ordering_users_liked_post.items():
            ordering = sorted(ordering, reverse=True)

            self._create_posts_with_likes(liked_users)

            recommended_posts = PostManager.get_recommended_posts(user)

            for post, likes_count in zip(recommended_posts, ordering):
                with self.subTest():
                    self.assertEqual(post.likes_count, likes_count)

            PostManager.delete_all_posts()

    def test_like_unlike_post(self):
        post = PostFactory()

        for user in self._test_users:
            PostManager.like_post(post, user)

            with self.subTest():
                self.assertIn(user, post.likes.all())

            PostManager.unlike_post(post, user)

            with self.subTest():
                self.assertNotIn(user, post.likes.all())


class TestUserManager(TestCase):
    def setUp(self) -> None:
        self._test_users = [UserFactory() for _ in range(10)]

    def test_get_only_users_data_has_additional_attr(self):
        users_from_manager = UserManager.get_only_users_data()

        for user in users_from_manager:
            with self.subTest():
                self.assertTrue(hasattr(user, 'followers_number'))
                self.assertTrue(hasattr(user, 'following_number'))
                self.assertTrue(hasattr(user, 'posts_number'))

    def test_follow_unfollow_user(self):
        test_user = UserFactory()

        for user in self._test_users:
            UserManager.follow_user(user, test_user)

            with self.subTest():
                self.assertIn(user, test_user.followers.all())

            UserManager.unfollow_user(user, test_user)

            with self.subTest():
                self.assertNotIn(user, test_user.followers.all())

    @staticmethod
    def _create_test_patterns_users_dict() -> dict:
        test_patterns_users = {
            'test': (
                UserFactory(username='testName'),
                UserFactory(username='testTest')
            ),

            'johny': (
                UserFactory(username='johny_crunch'),
                UserFactory(username='JoHny')
            ),

            'michael': (
                UserFactory(username='michael_'),
                UserFactory(username='MichaeL')
            )
        }

        return test_patterns_users

    def test_search_users_by_username(self):
        test_patterns_users = self._create_test_patterns_users_dict()

        for pattern, users in test_patterns_users.items():
            searched_users = UserManager.search_users_by_nickname(pattern)

            for user in users:
                with self.subTest():
                    self.assertIn(user, searched_users)


class TestCommentManager(TestCase):
    def setUp(self) -> None:
        self._test_users = [UserFactory() for _ in range(10)]

    def test_add_delete_comment(self):
        test_post = PostFactory()

        for user in self._test_users:
            new_comment = CommentManager.add_comment(
                user, test_post, 'Test text'
            )

            with self.subTest():
                self.assertIn(new_comment, models.Comment.objects.all())

            CommentManager.delete_comment(new_comment)

            with self.subTest():
                self.assertNotIn(new_comment, models.Comment.objects.all())
