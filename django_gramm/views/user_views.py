from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import  HttpResponseNotFound, JsonResponse

from django.views import View

from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

from django.views.generic.edit import UpdateView

from django_gramm.forms import UserEditForm

from django_gramm.models_manager import PostManager, UserManager, User


from django_gramm.views.mixins import SignInRequiredMixin


class UserProfile(SignInRequiredMixin, SingleObjectMixin, ListView):
    template_name = 'django_gramm/pages/profile.html'

    object = None
    posts = None

    slug_url_kwarg = 'user_slug'
    slug_field = 'username'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            queryset=UserManager.get_only_users_data()
        )

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user

        context['user_to_display'] = self.object
        context['posts'] = self.posts

        context['is_follow'] = self.request.user.following.filter(
            username=self.object.username
        ).exists()

        return context

    def get_queryset(self):
        self.posts = PostManager.get_posts_with_related_data_by_user(
            self.object
        )

        return self.posts


class EditUserProfile(SignInRequiredMixin, UpdateView):
    template_name = 'django_gramm/editing/profile_editing.html'

    model = User
    form_class = UserEditForm

    slug_url_kwarg = 'user_slug'
    slug_field = 'username'

    def form_valid(self, form):
        messages.success(self.request, 'Profile successfully edited')

        return super().form_valid(form)


class FollowUserJson(SignInRequiredMixin, View):
    @staticmethod
    def get(request, user_slug: str):
        if user_slug == (current_user := request.user).username:
            return JsonResponse({'status': 'ERROR', 'code': 403})

        user_to_follow = UserManager.get_user_with_followers(user_slug)

        UserManager.follow_user(current_user, user_to_follow)

        return JsonResponse({'status': 'OK', 'code': 200})


class UnfollowUserJson(SignInRequiredMixin, View):
    @staticmethod
    def get(request, user_slug: str):
        if user_slug == (current_user := request.user).username:
            return JsonResponse({'status': 'ERROR', 'code': 403})

        user_to_unfollow = UserManager.get_user_with_followers(user_slug)

        UserManager.unfollow_user(current_user, user_to_unfollow)

        return JsonResponse({'status': 'OK', 'code': 200})


class FollowViews(SignInRequiredMixin, ListView):
    context_object_name = 'users'

    user_to_display = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user_to_display'] = self.user_to_display

        return context


class ShowFollowers(FollowViews):
    template_name = 'django_gramm/pages/followers.html'

    def get_queryset(self):
        self.user_to_display = get_object_or_404(
            User, username=self.kwargs['user_slug']
        )

        return self.user_to_display.followers.all()


class ShowFollowing(FollowViews):
    template_name = 'django_gramm/pages/following.html'

    def get_queryset(self):
        self.user_to_display = get_object_or_404(
            User, username=self.kwargs['user_slug']
        )

        return self.user_to_display.following.all()


# TODO.
@login_required(login_url=reverse_lazy('django_gramm:login'))
def search_users(request):
    searched_users_nickname = None
    found_users = None

    if request.method == 'POST':
        searched_users_nickname = request.POST['searched_users']

        if searched_users_nickname:
            found_users = UserManager.search_users_by_nickname(
                searched_users_nickname
            )

    return render(
        request, 'django_gramm/pages/search_users.html',
        {'searched_users': searched_users_nickname, 'users': found_users}
    )
