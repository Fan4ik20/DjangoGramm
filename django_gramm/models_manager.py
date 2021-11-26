from typing import List, Union

from django.db.models import Count, F, QuerySet

from .models import Post, User, Photo, Comment


class PostManager:
    @staticmethod
    def _create_post_instance(user: User, description: str) -> Post:
        return Post.objects.create(user=user, description=description)

    @staticmethod
    def _link_photo_to_post(post: Post, post_image) -> Photo:
        return Photo.objects.create(post=post, post_image=post_image)

    @classmethod
    def create_new_post(cls, user: User, post_image, description: str) -> Post:
        post = cls._create_post_instance(user, description)
        cls._link_photo_to_post(post, post_image)

        return post

    @staticmethod
    def get_posts() -> Union[QuerySet, List[Post]]:
        posts = Post.objects.prefetch_related('photo_to_post')

        return posts

    @staticmethod
    def get_posts_with_related_data() -> Union[QuerySet, List[Post]]:
        posts = PostManager.get_posts().select_related(
            'user'
        ).prefetch_related(
            'likes'
        ).prefetch_related(
            'comments'
        ).prefetch_related(
            'comments__user'
        ).annotate(
            likes_count=Count('likes', distinct=True),
        )

        return posts

    @staticmethod
    def get_post_with_related_data(post_id: int) -> Post:
        return PostManager.get_posts_with_related_data().get(pk=post_id)

    @staticmethod
    def get_posts_with_comments():
        posts = Post.objects.prefetch_related(
            'comments'
        ).select_related('user')

        return posts

    @staticmethod
    def get_posts_with_annotated_data() -> Union[QuerySet, List[Post]]:
        posts = PostManager.get_posts().select_related(
            'user'
        ).annotate(
            likes_count=Count(F('likes'), distinct=True),
            comments_count=Count(F('comments'), distinct=True)
        )

        return posts

    @staticmethod
    def get_posts_with_related_data_by_user(
            user: User
    ) -> Union[QuerySet, List[Post]]:

        posts = PostManager.get_posts_with_annotated_data().filter(
            user=user
        ).order_by('-created_date')

        return posts

    @staticmethod
    def get_recommended_posts(user: User) -> Union[QuerySet, List[Post]]:
        posts = PostManager.get_posts_with_annotated_data().exclude(
            user=user
        ).order_by('-likes_count')[:15]

        return posts

    @staticmethod
    def get_following_users_posts(
            follower: User) -> Union[QuerySet, List[Post]]:

        posts = Post.objects.all().extra(select={
            'is_liked': (
                'select true from "django_gramm_post_likes" '
                'where post_id=django_gramm_post.id '
                'and django_gramm_post_likes.user_id = %s'
            )
        },
            select_params=(follower.id,)
        ).prefetch_related(
            'photo_to_post'
        ).select_related('user')

        return posts

    @staticmethod
    def like_post(post: Post, user: User) -> None:
        post.likes.add(user)

    @staticmethod
    def unlike_post(post: Post, user: User) -> None:
        post.likes.remove(user)

    @staticmethod
    def delete_post(post: Post):
        post.delete()

    @staticmethod
    def delete_all_posts():
        Post.objects.all().delete()


class UserManager:
    @staticmethod
    def get_only_users_data() -> Union[QuerySet, List[User]]:
        users = User.objects.annotate(
            followers_number=Count('followers', distinct=True),
            following_number=Count('following', distinct=True),
            posts_number=Count('posts', distinct=True),
        )

        return users

    @staticmethod
    def get_user_with_aggregated_data(user_slug: str) -> User:
        return UserManager.get_only_users_data(

        ).get(username=user_slug)

    @staticmethod
    def get_user_with_followers(user_slug: str) -> User:
        user = User.objects.prefetch_related(
            'followers'
        ).get(username=user_slug)

        return user

    @staticmethod
    def unfollow_user(follower: User, followed: User) -> None:
        followed.followers.remove(follower)

        followed.save()

    @staticmethod
    def follow_user(follower: User, followed: User) -> None:
        followed.followers.add(follower)

        followed.save()

    @staticmethod
    def get_following_users_with_all_related_data(
            follower: User) -> Union[QuerySet, List[User]]:

        followings = follower.following.prefetch_related(
            'posts'
        ).prefetch_related(
            'posts__photo_to_post'
        ).order_by('posts__created_date')

        return followings

    @staticmethod
    def search_users_by_nickname(nickname: str) -> Union[QuerySet, List[User]]:
        found_users = User.objects.filter(username__icontains=nickname)

        return found_users

    @staticmethod
    def delete_all_users():
        User.objects.all().delete()


class CommentManager:
    @staticmethod
    def add_comment(user: User, post: Post, content: str) -> Comment:
        comment = Comment.objects.create(
            user=user, post=post, content=content
        )

        return comment

    @staticmethod
    def delete_comment(comment: Comment) -> None:
        comment.delete()
