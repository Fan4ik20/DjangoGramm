from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.test import TestCase, RequestFactory, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files import File

from django_gramm.tests.factories import (
    CommentFactory, UserFactory, PostFactory,
    create_posts_using_factories, create_post_using_factories
)
from django_gramm.models_manager import UserManager, PostManager

from django_gramm import views
from django_gramm import models


class TestViews(TestCase):
    def setUp(self) -> None:
        self._request_factory = RequestFactory()

        self._test_users = [UserFactory() for _ in range(10)]
        self._test_posts = create_posts_using_factories(self._test_users)

    def tearDown(self) -> None:
        PostManager.delete_all_posts()
        UserManager.delete_all_users()

    @staticmethod
    def _add_necessary_attributes_to_request(request: HttpRequest) -> None:
        SessionMiddleware().process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        request._messages = messages


class TestGeneralViews(TestViews):
    def test_index_view(self):
        test_following = self._test_users[:5]
        test_user = UserFactory.create(following=test_following)
        test_posts = self._test_posts[:5]

        request = self._request_factory.get(reverse('django_gramm:index'))
        request.user = test_user

        response = views.index(request)

        for post in test_posts:
            with self.subTest():
                self.assertEqual(response.status_code, 200)
                self.assertIn(
                    bytes(post.get_absolute_url(), encoding='utf-8'),
                    response.content
                )

    def test_index_view_with_empty_posts(self):
        PostManager.delete_all_posts()

        test_following = self._test_users[:5]
        test_user = UserFactory.create(following=test_following)

        request = self._request_factory.get(reverse('django_gramm:index'))
        request.user = test_user

        response = views.index(request)

        self.assertIn(b"Sorry, there is no posts yet.", response.content)
        self.assertEqual(response.status_code, 200)


apps_for_mock = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'debug_toolbar',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'storages',

    'easy_thumbnails',

    'factory',

    'django_gramm.apps.DjangoGrammConfig',
]


class TestUserViews(TestViews):
    def setUp(self) -> None:
        super().setUp()

        self._client = Client()

    def _create_request_for_registration(
            self, registration_data: dict) -> HttpRequest:
        request = self._request_factory.post(
            reverse('django_gramm:registration'),
            registration_data
        )
        self._add_necessary_attributes_to_request(request)

        request.user = AnonymousUser()

        return request

    def test_user_registration_post_with_valid_data(self):
        user_data = {
            'username': 'TestRegistrationUser',
            'email': 'test@test.com',
            'password1': 'Z_w312613242',
            'password2': 'Z_w312613242',
        }

        request = self._create_request_for_registration(user_data)

        response = views.UserRegistrationView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/confirm-email/')

        self.assertTrue(
            models.User.objects.get(username=user_data['username'])
        )

    def test_user_registration_post_with_invalid_data_not_create_user(self):
        user_data = {}

        request = self._create_request_for_registration(user_data)

        views.UserRegistrationView.as_view()(request)

        self.assertEqual(models.User.objects.count(), len(self._test_users))

    def _create_request_for_test_user_login(
            self, login_data: dict) -> HttpRequest:

        request = self._request_factory.post(
            reverse('django_gramm:login'), login_data
        )
        self._add_necessary_attributes_to_request(request)

        request.user = AnonymousUser()

        return request

    @override_settings(ACCOUNT_EMAIL_VERIFICATION='optional')
    def test_user_login_post(self):
        test_user = UserFactory(
            username='TestLoginUsername'
        )
        test_user.set_password('Z3_123s1521')
        test_user.save()

        login_data = {
            'login': test_user.username, 'password': 'Z3_123s1521'
        }

        request = self._create_request_for_test_user_login(login_data)

        response = views.UserLoginView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('django_gramm:index'))

        self.assertTrue(request.user.is_authenticated)

    def _create_request_for_test_logout(
            self, user: models.User) -> HttpRequest:

        request = self._request_factory.get(reverse('django_gramm:logout'))
        self._add_necessary_attributes_to_request(request)

        request.user = user

        return request

    @override_settings(ACCOUNT_EMAIL_VERIFICATION='optional')
    def test_user_logout(self):
        test_user = UserFactory(
            username='TestLoginUsername', password='Z3_123s1521'
        )

        request = self._create_request_for_test_logout(test_user)
        self.assertTrue(request.user.is_authenticated)

        response = views.user_logout(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('django_gramm:login'))

        self.assertFalse(request.user.is_authenticated)

    def _create_request_for_show_user_profile(
            self, test_user: models.User, user_to_display: models.User
    ) -> HttpRequest:

        request = self._request_factory.get(
            reverse(
                'django_gramm:user_profile', args=[user_to_display.username]
            )
        )
        self._add_necessary_attributes_to_request(request)

        request.user = test_user

        return request

    def test_show_user_profile_other_user(self):
        test_user = UserFactory()

        user_to_display = self._test_users[0]
        users_posts = [
            create_post_using_factories(user_to_display) for _ in range(5)
        ]

        request = self._create_request_for_show_user_profile(
            test_user, user_to_display
        )
        response = views.show_user_profile(request, user_to_display.username)

        content = response.content

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Follow', content)

        for post in users_posts:
            with self.subTest():
                self.assertIn(
                    bytes(post.get_absolute_url(), encoding='utf-8'), content
                )

    def test_show_user_profile_owner(self):
        test_user = self._test_users[0]

        request = self._create_request_for_show_user_profile(
            test_user, test_user
        )

        response = views.show_user_profile(request, test_user.username)
        content = response.content

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Profile', content)

    def _create_request_for_edit_user_profile(
            self, user: models.User, edit_data: dict) -> HttpRequest:

        request = self._request_factory.post(
            reverse('django_gramm:edit_profile', args=[user.username]),
            edit_data
        )
        self._add_necessary_attributes_to_request(request)

        request.user = user

        return request

    def test_edit_user_profile_post_with_valid_data(self):
        test_user = self._test_users[0]
        data_to_change = {
            'username': 'TestUsernameForEditing',
            'email': 'testEdit@test.com'
        }

        request = self._create_request_for_edit_user_profile(
            test_user, data_to_change
        )

        response = views.edit_user_profile(request, test_user.username)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(request.user.username, data_to_change['username'])
        self.assertEqual(request.user.email, data_to_change['email'])

    def _create_request_for_change_user_password(
            self, user: models.User, password_change_data: dict
    ) -> HttpRequest:

        request = self._request_factory.post(
            reverse('django_gramm:change_password'),
            password_change_data
        )
        self._add_necessary_attributes_to_request(request)

        request.user = user

        return request

    def test_change_user_password(self):
        test_user = UserFactory()
        test_user.set_password('Z3_123s1521')

        password_change_data = {
            'old_password': 'Z3_123s1521', 'new_password1': 'Z4_223s12131',
            'new_password2': 'Z4_223s12131'
        }

        request = self._create_request_for_change_user_password(
            test_user, password_change_data
        )

        response = views.change_user_password(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, reverse(
                'django_gramm:edit_profile', args=[test_user.username]
            )
        )
        self.assertTrue(
            request.user.check_password(password_change_data['new_password1'])
        )

    def test_follow_user(self):
        test_user = self._test_users[0]

        self._client.force_login(test_user)

        for user in self._test_users[1:]:
            response = self._client.get(
                reverse('django_gramm:follow', args=[user.username])
            )
            content = response.content

            with self.subTest():
                self.assertEqual(response.status_code, 200)

                self.assertJSONEqual(
                    content.decode(encoding='utf-8'),
                    {'status': 'OK', 'code': 200}
                )

                self.assertIn(test_user, user.followers.all())

    def test_unfollow_user(self):
        test_user = UserFactory(followers=self._test_users)

        for user in self._test_users:
            self._client.force_login(user)

            response = self._client.get(reverse(
                'django_gramm:unfollow', args=[test_user.username]
            ))
            content = response.content

            self._client.logout()

            with self.subTest():
                self.assertEqual(response.status_code, 200)

                self.assertJSONEqual(
                    content.decode(encoding='utf-8'),
                    {'status': 'OK', 'code': 200}
                )

                self.assertNotIn(user, test_user.followers.all())

    def test_show_followers(self):
        test_user = UserFactory(followers=self._test_users)

        self._client.force_login(test_user)

        response = self._client.get(
            reverse('django_gramm:followers', args=[test_user.username])
        )

        self.assertTrue(response.status_code, 200)

        content = response.content

        for user in self._test_users:
            with self.subTest():
                self.assertIn(
                    bytes(user.get_absolute_url(), encoding='utf-8'), content
                )

    def test_show_following(self):
        test_user = UserFactory(following=self._test_users)

        self._client.force_login(test_user)

        response = self._client.get(
            reverse('django_gramm:following', args=[test_user.username])
        )

        self.assertTrue(response.status_code, 200)

        content = response.content

        for user in self._test_users:
            with self.subTest():
                self.assertIn(
                    bytes(user.get_absolute_url(), encoding='utf-8'), content
                )

    def test_search_users(self):
        self._client.force_login(self._test_users[0])

        users_to_search = {
            'John': (
                UserFactory(username='John'), UserFactory(username='Johnny'),
                UserFactory(username='johnathan')
            ),

            'Mi': (
                UserFactory(username='MikoNiko'), UserFactory(username='Mimi'),
                UserFactory(username='MichaelMan')
            ),

            'Ka': (
                UserFactory(username='KarKarych'),
                UserFactory(username='Kata'), UserFactory(username='Kamil')
            )
        }

        for pattern, expected_users in users_to_search.items():
            response = self._client.post(
                reverse('django_gramm:search_users'),
                {'searched_users': pattern}
            )

            content = response.content

            with self.subTest():
                self.assertEqual(response.status_code, 200)

                for user in expected_users:
                    self.assertIn(
                        bytes(user.get_absolute_url(), encoding='utf-8'),
                        content
                    )

    def test_search_users_with_empty_searched_users(self):
        self._client.force_login(self._test_users[0])

        response = self._client.post(
            reverse('django_gramm:search_users'), {'searched_users': ''}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You forgot to search for a somebody', response.content)

    def test_search_users_with_empty_users(self):
        UserManager.delete_all_users()

        test_user = UserFactory(username='Test')
        self._client.force_login(test_user)

        patterns = ['ka', 'john', 'ivan', 'shrek']

        for pattern in patterns:
            response = self._client.post(
                reverse('django_gramm:search_users'),
                {'searched_users': pattern}
            )

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Sorry, there are no users', response.content)


class TestPostsViews(TestViews):
    def _create_request_for_show_post(
            self, user: models.User, post: models.Post) -> HttpRequest:
        request = self._request_factory.get(
            reverse('django_gramm:show_post', args=[user.username, post.pk])
        )
        self._add_necessary_attributes_to_request(request)

        request.user = user

        return request

    def _test_post_data_for_show_post(
            self, test_post: models.Post, content: bytes) -> None:

        with self.subTest():
            self.assertIn(
                bytes(test_post.user.get_absolute_url(), encoding='utf-8'),
                content
            )

            self.assertIn(
                bytes(test_post.user.username, encoding='utf-8'), content
            )

            if test_post.description:
                self.assertIn(bytes(test_post.description, encoding='utf-8'),
                              content)

    def _test_comments_for_show_post(
            self, test_comments: list, content: bytes) -> None:

        for comment in test_comments:
            with self.subTest():
                self.assertIn(
                    bytes(comment.content, encoding='utf-8'), content
                )

                self.assertIn(
                    bytes(comment.user.get_absolute_url(), encoding='utf-8'),
                    content
                )

                self.assertIn(
                    bytes(comment.user.username, encoding='utf-8'), content
                )


    def _test_is_liked_for_show_post(
            self, request: HttpRequest, users_post: models.User,
            post: models.Post, users: list) -> None:

        for index, user in enumerate(users):
            request.user = user

            response = views.show_post(request, users_post.username, post.pk)
            content = response.content

            if post in user.liked_posts.all():
                self.assertIn(
                    bytes('alt="unlike"', encoding='utf-8'), content
                )

            else:
                self.assertIn(
                    bytes('alt="like"', encoding='utf-8'), content
                )

    def test_show_post(self):
        users_post = self._test_users[0]

        test_post = PostFactory(user=users_post, likes=self._test_users[:5])
        test_comments = [
            CommentFactory(
                user=users_post, post=test_post
            ) for _ in range(5)
        ]

        request = self._create_request_for_show_post(
            test_post.user, test_post
        )

        response = views.show_post(
            request, test_post.user.username, test_post.pk
        )
        content = response.content

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            bytes(users_post.username, encoding='utf-8'), content
        )

        self._test_post_data_for_show_post(test_post, content)
        self._test_comments_for_show_post(test_comments, content)
        self._test_is_liked_for_show_post(
            request, users_post, test_post, self._test_users
        )

    def _create_request_for_test_delete_post(
            self, user: models.User, post: models.Post) -> HttpRequest:

        request = self._request_factory.get(
            reverse('django_gramm:delete_post', args=[user.username, post.pk])
        )
        self._add_necessary_attributes_to_request(request)

        request.user = user

        return request

    def test_delete_post(self):
        test_user = self._test_users[0]
        test_post = self._test_posts[0]

        request = self._create_request_for_test_delete_post(
            test_user, test_post
        )

        response = views.delete_post(request, test_user.username, test_post.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse('django_gramm:user_profile', args=[test_user.username])
        )

        self.assertFalse(models.Post.objects.filter(pk=test_post.pk).exists())

    def test_delete_post_with_incorrect_user(self):
        test_user = self._test_users[1]
        test_post = self._test_posts[0]

        request = self._create_request_for_test_delete_post(
            test_user, test_post
        )

        response = views.delete_post(
            request, test_post.user.username, test_post.pk
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            models.Post.objects.filter(pk=test_post.pk).exists()
        )

    def _create_request_for_test_add_comment(
            self, post_user: models.User, post: models.Post,
            comment_user: models.User, comment_data: dict) -> HttpRequest:

        request = self._request_factory.post(
            reverse(
                'django_gramm:add_comment', args=[post_user.username, post.pk]
            ),
            comment_data
        )
        self._add_necessary_attributes_to_request(request)

        request.user = comment_user

        return request

    def test_add_comment_post(self):
        test_post = self._test_posts[0]
        comment_user = self._test_users[1]

        comment_data = {
            'content': 'TestContentForTestComment'
        }

        request = self._create_request_for_test_add_comment(
            test_post.user, test_post, comment_user, comment_data
        )

        response = views.add_comment_to_post_json(
            request, test_post.user.username, test_post.pk
        )
        content = response.content

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(
            content.decode(encoding='utf-8'),
            {'status': 'OK', 'code': 200}
        )

        self.assertTrue(
            models.Comment.objects.filter(
                post=test_post, user=comment_user,
                content=comment_data['content']
            ).exists()
        )

    def _create_request_for_test_delete_comment(
            self, post_user: models.User, post: models.Post,
            comment_user: models.User, comment: models.Comment) -> HttpRequest:

        request = self._request_factory.delete(
            reverse(
                'django_gramm:delete_comment',
                args=[post_user.username, post.pk, comment.pk]
            )
        )

        self._add_necessary_attributes_to_request(request)

        request.user = comment_user

        return request

    def test_delete_comment(self):
        test_post = self._test_posts[0]

        comment_user = self._test_users[1]
        test_comment = CommentFactory(user=comment_user, post=test_post)

        request = self._create_request_for_test_delete_comment(
            test_post.user, test_post, comment_user, test_comment
        )

        response = views.delete_comment_json(
            request, test_post.user.username, test_post.pk, test_comment.pk
        )
        content = response.content

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(
            content.decode(encoding='utf-8'),
            {'status': 'OK', 'code': 200}
        )

        self.assertFalse(
            models.Comment.objects.filter(
                pk=test_comment.pk
            ).exists()
        )

    def _test_delete_comment_with_incorrect_data(
            self, post_user: models.User, test_post: models.Post,
            comment_user: models.User, test_comment: models.Comment) -> None:

        request = self._create_request_for_test_delete_comment(
            test_post.user, test_post, comment_user, test_comment
        )

        response = views.delete_comment(
            request, post_user.username,
            test_post.pk, test_comment.pk
        )

        self.assertEqual(response.status_code, 403)

        self.assertTrue(
            models.Comment.objects.filter(
                pk=test_comment.pk
            ).exists()
        )

    def test_delete_comment_with_incorrect_user(self):
        incorrect_user = self._test_users[1]

        test_post = self._test_posts[2]
        test_comment = CommentFactory(
            user=self._test_users[0], post=test_post
        )

        self._test_delete_comment_with_incorrect_data(
            test_post.user, test_post, incorrect_user, test_comment
        )

    def test_delete_comment_with_incorrect_comment(self):
        test_post = self._test_posts[0]
        comment_user = self._test_users[1]

        test_comment = CommentFactory(
            user=comment_user, post=self._test_posts[1]
        )

        self._test_delete_comment_with_incorrect_data(
            test_post.user, test_post, comment_user, test_comment
        )

    def _create_request_for_test_add_post(
            self, user: models.User, post_data: dict) -> HttpRequest:

        request = self._request_factory.post(
            reverse('django_gramm:add_post', args=[user.username]),
            post_data
        )
        self._add_necessary_attributes_to_request(request)

        request.user = user

        return request

    def _add_post_data_to_request_test_add_post(
            self, user: models.User) -> HttpRequest:

        with open(
                'django_gramm/tests/test_files/test_photo.jpeg', 'rb'
        ) as test_photo:
            django_photo = File(test_photo)

            post_data = {
                'post_image': django_photo, 'description': 'TestDescription'
            }

            request = self._create_request_for_test_add_post(
                user, post_data
            )

        return request

    def test_add_post(self):
        test_user = UserFactory()

        self.assertFalse(test_user.posts.all().exists())

        request = self._add_post_data_to_request_test_add_post(test_user)

        response = views.add_post(request, test_user.username)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(test_user.posts.all().exists())

    def test_add_post_with_incorrect_user(self):
        test_user = UserFactory()

        self.assertFalse(test_user.posts.all().exists())

        request = self._add_post_data_to_request_test_add_post(test_user)

        response = views.add_post(request, self._test_users[0])

        self.assertEqual(response.status_code, 403)

        self.assertFalse(test_user.posts.all().exists())

    def _create_request_for_test_like_post_on_index(
            self, user: models.User, post: models.Post) -> HttpRequest:

        request = self._request_factory.get(
            reverse('django_gramm:like_post_on_index', args=[post.pk])
        )
        self._add_necessary_attributes_to_request(request)

        request.user = user

        return request

    def _create_request_for_test_unlike_post_on_index(
            self, user: models.User, post: models.Post) -> HttpRequest:

        request = self._request_factory.get(
            reverse('django_gramm:unlike_post_on_index', args=[post.pk])
        )
        self._add_necessary_attributes_to_request(request)

        request.user = user

        return request

    def _test_like_post_on_index(
            self, user: models.User, post: models.Post) -> None:

        request = self._create_request_for_test_like_post_on_index(
            user, post
        )

        response = views.like_post_on_index(request, post.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('django_gramm:index'))

        self.assertIn(user, post.likes.all())

    def _test_unlike_post_on_index(
            self, user: models.User, post: models.Post) -> None:

        request = self._create_request_for_test_unlike_post_on_index(
            user, post
        )

        response = views.unlike_post_on_index(request, post.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('django_gramm:index'))

        self.assertNotIn(user, post.likes.all())

    def test_like_unlike_post_on_index(self):
        test_post = self._test_posts[0]

        for user in self._test_users:
            self._test_like_post_on_index(user, test_post)
            self._test_unlike_post_on_index(user, test_post)

    def _create_request_for_like_post(
            self, user: models.User, post: models.Post) -> HttpRequest:

        request = self._request_factory.get(
            reverse('django_gramm:like_post',
                    args=[post.user.username, post.pk])
        )
        self._add_necessary_attributes_to_request(request)

        request.user = user

        return request

    def _create_request_for_unlike_post(
            self, user: models.User, post: models.Post) -> HttpRequest:

        request = self._request_factory.get(
            reverse('django_gramm:unlike_post',
                    args=[post.user.username, post.pk])
        )
        self._add_necessary_attributes_to_request(request)

        request.user = user

        return request

    def _test_like_post(self, user: models.User, post: models.Post) -> None:
        request = self._create_request_for_like_post(user, post)

        response = views.like_post_json(request, post.user.username, post.pk)
        content = response.content

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(
            content.decode(encoding='utf-8'),
            {'status': 'OK', 'code': 200}
        )

        self.assertIn(user, post.likes.all())

    def _test_unlike_post(self, user: models.User, post: models.Post) -> None:
        request = self._create_request_for_unlike_post(user, post)

        response = views.unlike_post_json(request, post.user.username, post.pk)
        content = response.content

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(
            content.decode(encoding='utf-8'),
            {'status': 'OK', 'code': 200}
        )

        self.assertNotIn(user, post.likes.all())

    def test_like_unlike_post(self):
        test_post = self._test_posts[0]

        for user in self._test_users:
            self._test_like_post(user, test_post)
            self._test_unlike_post(user, test_post)
