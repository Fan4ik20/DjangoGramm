from django import template

from django_gramm.models import Post, User

register = template.Library()


@register.simple_tag()
def is_liked(post: Post, user: User) -> bool:
    return post.likes.filter(username=user.username).exists()
