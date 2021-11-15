from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import (
    HttpResponseForbidden, JsonResponse
)

from django.views import View
from django.views.generic import (
    ListView, DetailView, DeleteView,
    TemplateView, FormView
)
from django.views.generic.edit import BaseFormView

from django_gramm.forms import PhotoForm, PostForm, CommentForm

from django_gramm.models_manager import (
    PostManager, CommentManager,
    Post, Comment
)

from django_gramm.views.mixins import SignInRequiredMixin


class Index(SignInRequiredMixin, ListView):
    template_name = 'django_gramm/pages/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return PostManager.get_following_users_posts(self.request.user)


class RecommendedPosts(SignInRequiredMixin, ListView):
    template_name = 'django_gramm/pages/recommended_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return PostManager.get_recommended_posts(self.request.user)


class PostDetail(SignInRequiredMixin, DetailView):
    template_name = 'django_gramm/pages/show_post.html'

    context_object_name = 'post'

    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return PostManager.get_posts_with_related_data()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = context['post']

        context['users_post'] = post.user.username

        context['photos'] = post.photo_to_post.all()

        context['comments'] = post.comments.all()
        context['comment_form'] = CommentForm()

        context['is_liked'] = post.likes.filter(
            username=self.request.user.username
        ).exists()

        return context


class DeletePost(SignInRequiredMixin, DeleteView):
    model = Post

    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse_lazy(
            'django_gramm:user_profile', args=(self.kwargs['user_slug'],)
        )

    def post(self, request, *args, **kwargs):
        if request.user.username != self.kwargs['user_slug']:
            return HttpResponseForbidden()

        messages.success(request, 'The post was successfully deleted')

        return super().post(request, *args, **kwargs)


class AddCommentToPostJson(SignInRequiredMixin, BaseFormView):
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])

        content = form.cleaned_data['content']

        CommentManager.add_comment(self.request.user, post, content)

        return JsonResponse({'status': 'OK', 'code': 200})

    def form_invalid(self, form):
        return JsonResponse({'status': 'ERROR', 'code': 400})


# Fixme.
class DeleteCommentJson(SignInRequiredMixin, View):
    @staticmethod
    def post(
            request, user_slug: str, post_id: int, comment_id: int):

        if request.method != 'POST':
            return JsonResponse({'status': 'ERROR', 'code': 404})

        post = get_object_or_404(PostManager.get_posts_with_comments(),
                                 pk=post_id)
        comment = get_object_or_404(Comment, pk=comment_id)

        if request.user != post.user and request.user != comment.user:
            return JsonResponse({'status': 'ERROR', 'code': 403})

        if comment not in post.comments.all():
            return JsonResponse({'status': 'ERROR', 'code': 403})

        CommentManager.delete_comment(comment)

        messages.success(request, 'The comment was successfully deleted')

        return JsonResponse({'status': 'OK', 'code': 200})


# FIXME.
class AddPost(SignInRequiredMixin, FormView):
    form_class = PostForm
    second_form_class = PhotoForm

    template_name = 'django_gramm/pages/add_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['post_form'] = self.form_class()

        context['photo_form'] = self.second_form_class()

        return context

    def get(self, request, *args, **kwargs):
        if request.user.username != self.kwargs['user_slug']:
            return HttpResponseForbidden()

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.username != self.kwargs['user_slug']:
            return HttpResponseForbidden()

        post_form = self.get_form()
        photo_form = self.second_form_class(
            self.request.POST, self.request.FILES
        )

        if post_form.is_valid() and photo_form.is_valid():
            new_post = PostManager.create_new_post(
                user=request.user,
                **post_form.cleaned_data, **photo_form.cleaned_data
            )

            messages.success(request, 'The post was successfully created')

            return redirect(new_post)

        else:
            messages.error(request, 'Error adding post')


class LikePostJson(SignInRequiredMixin, View):
    @staticmethod
    def get(request, user_slug: str, post_id: int):
        post = get_object_or_404(Post, pk=post_id)

        PostManager.like_post(post, request.user)

        return JsonResponse({'status': 'OK', 'code': 200})


class UnLikePostJson(SignInRequiredMixin, View):
    @staticmethod
    def get(request, user_slug: str, post_id: int):
        post = get_object_or_404(Post, pk=post_id)

        PostManager.unlike_post(post, request.user)

        return JsonResponse({'status': 'OK', 'code': 200})


class ShowUserDirect(SignInRequiredMixin, TemplateView):
    template_name = 'django_gramm/direct/inbox.html'
