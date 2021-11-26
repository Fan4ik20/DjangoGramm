from django.urls import path

from django_gramm.views import (
    auth_views, post_views, user_views
)

from django.views.generic import TemplateView

from allauth.socialaccount.views import SignupView as SignUpOauth

app_name = 'django_gramm'

urlpatterns = [
    path('', post_views.Index.as_view(), name='index'),

    # Auth.
    path('accounts/signup/', auth_views.UserRegistration.as_view(),
         name='registration'),
    path(
        'accounts/confirm-email/',
        auth_views.UserEmailVerificationSentView.as_view(),
        name='account_email_verification_sent'
    ),

    path('accounts/login/', auth_views.UserLogin.as_view(), name='login'),
    path('accounts/logout/', auth_views.UserLogout.as_view(), name='logout'),

    path(
        'accounts/social/signup/', auth_views.UserRegistrationOauth.as_view(),
    ),

    # User pages.
    path(
        'users/search/', user_views.search_users, name='search_users'
    ),

    path(
        'users/<slug:user_slug>/', user_views.UserProfile.as_view(),
        name='user_profile'
    ),

    path(
        'users/<slug:user_slug>/edit/', user_views.EditUserProfile.as_view(),
        name='edit_profile'
    ),

    path(
        'users/<slug:user_slug>/password/',
        auth_views.ChangeUserPassword.as_view(),
        name='change_password'
    ),

    # Password Resetting.
    path(
        'reset_password/',
        auth_views.UserPasswordReset.as_view(), name='password_reset'
    ),
    path(
        'password_reset_sent/',
        auth_views.UserPasswordResetDone.as_view(), name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.UserPasswordResetConfirm.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'password_reset_complete/',
        auth_views.UserPasswordResetComplete.as_view(),
        name='password_reset_complete'
    ),

    # Follow related pages.
    path('users/<slug:user_slug>/follow/', user_views.FollowUserJson.as_view(),
         name='follow'),

    path(
        'users/<slug:user_slug>/unfollow/',
        user_views.UnfollowUserJson.as_view(),
        name='unfollow'
    ),

    path(
        'users/<slug:user_slug>/followers/',
        user_views.ShowFollowers.as_view(),
        name='followers'
    ),

    path(
        'users/<slug:user_slug>/followings/',
        user_views.ShowFollowing.as_view(),
        name='following'
    ),

    # Post functions.
    path(
        'users/<slug:user_slug>/posts/create/',
        post_views.AddPost.as_view(), name='add_post'
    ),

    path(
        'users/<slug:user_slug>/posts/<int:post_id>/',
        post_views.PostDetail.as_view(), name='show_post'
    ),

    path(
        'users/<slug:user_slug>/posts/<int:post_id>/delete/',
        post_views.DeletePost.as_view(), name='delete_post'
    ),

    path(
        'users/<slug:user_slug>/posts/<int:post_id>/like/',
        post_views.LikePostJson.as_view(),
        name='like_post'
    ),

    path(
        'users/<slug:user_slug>/posts/<int:post_id>/unlike/',
        post_views.UnLikePostJson.as_view(),
        name='unlike_post'
    ),

    path(
        'users/<slug:user_slug>/posts/<int:post_id>/add_comment/',
        post_views.AddCommentToPostJson.as_view(), name='add_comment'
    ),

    path(
        'users/<slug:user_slug>/posts/<int:post_id>/comments/<int:comment_id>/'
        'delete/',
        post_views.DeleteCommentJson.as_view(), name='delete_comment'
    ),

    path(
        'posts/recommended/', post_views.RecommendedPosts.as_view(),
        name='recommended_posts'
    ),

    path(
        'direct/<slug:user_slug>/', post_views.ShowUserDirect.as_view(),
        name='direct'
    ),

    path(
        'test/',
        TemplateView.as_view(template_name='django_gramm/post_test.html')
    )
]
