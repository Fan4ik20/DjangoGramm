from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global

saved_file.connect(generate_aliases_global)


def _create_place_to_save_user_picture(user: 'User', filename):
    return f'users/{user.username}/profile_pictures/{filename}'


class User(AbstractUser):
    email = models.EmailField(unique=True)

    description = models.CharField(max_length=40, blank=True)

    picture = models.ImageField(
        upload_to=_create_place_to_save_user_picture, blank=True
    )

    followers = models.ManyToManyField(
        'self', symmetrical=False, blank=True,
        related_name='following'
    )

    def get_absolute_url(self):
        return reverse('django_gramm:user_profile', args=(self.username,))

    def __str__(self):
        return f'{self.pk} - {self.username}'


class BlockedUserList(models.Model):
    user_id = models.OneToOneField(
        'User', on_delete=models.CASCADE, primary_key=True,
        related_name='blocked_users_list'
    )

    blocked_users = models.ForeignKey('User', on_delete=models.CASCADE)


class Post(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='posts'
    )

    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(
        'User', symmetrical=False, related_name='liked_posts', blank=True
    )

    def get_absolute_url(self):
        return reverse(
            'django_gramm:show_post',
            kwargs={'user_slug': self.user.username, 'post_id': self.pk}
        )

    def __str__(self):
        return f'Post id: {self.pk}, user - {self.user}'

    class Meta:
        ordering = '-created_date',


def _create_place_to_save_photo(photo_instance: 'Photo', filename: str):
    return (f'users/{photo_instance.post.user.username}/post_photos/'
            f'/post_{photo_instance.post.id}/{filename}')


class Photo(models.Model):
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE,
        related_name='photo_to_post'
    )

    post_image = models.ImageField(
        upload_to=_create_place_to_save_photo
    )

    def __str__(self):
        return f'Image url - {self.post_image.url}, post id - {self.post.id}'


class Comment(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='comments'
    )

    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='comments'
    )

    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
