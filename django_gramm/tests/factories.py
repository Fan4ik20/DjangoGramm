from factory.django import DjangoModelFactory
from factory.django import ImageField as FactoryImageField
import factory

from django_gramm import models


class UserFactory(DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Faker('user_name')
    email = factory.Faker('ascii_email')
    password = factory.Faker('password')

    @factory.post_generation
    def followers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for follower in extracted:
                self.followers.add(follower)

    @factory.post_generation
    def following(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for following in extracted:
                self.following.add(following)


class PostFactory(DjangoModelFactory):
    class Meta:
        model = models.Post

    user = factory.SubFactory(UserFactory)
    description = factory.Faker('sentence')

    @factory.post_generation
    def likes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for liked_user in extracted:
                self.likes.add(liked_user)


class PhotoFactory(DjangoModelFactory):
    class Meta:
        model = models.Photo

    post = factory.SubFactory(PostFactory)
    post_image = FactoryImageField()


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = models.Comment

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)

    content = factory.Faker('sentence')


def create_post_using_factories(user: models.User) -> models.Post:
    post = PostFactory(user=user)
    PhotoFactory(post=post)

    return post


def create_posts_using_factories(users_list: list) -> list:
    posts = [
        create_post_using_factories(user) for user in users_list
    ]

    return posts
