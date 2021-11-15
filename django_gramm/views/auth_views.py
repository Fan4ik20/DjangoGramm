from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

import allauth.account.views as account_views

from django_gramm.forms import (
    PasswordEditForm, UserPasswordResetForm,
    UserPasswordResetConfirmForm, AccountUserLoginForm,
    AccountRegistrationForm
)

from django_gramm.views.mixins import SignInRequiredMixin


class UserRegistration(account_views.SignupView):
    form_class = AccountRegistrationForm

    template_name = 'django_gramm/auth/account_registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['login_url'] = reverse_lazy('django_gramm:login')

        return context


class UserLogin(account_views.LoginView):
    form_class = AccountUserLoginForm

    template_name = 'django_gramm/auth/account_login.html'

    success_url = reverse_lazy('django_gramm:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['signup_url'] = reverse_lazy('django_gramm:registration')

        return context


class UserLogout(SignInRequiredMixin, auth_views.LogoutView):
    template_name = 'django_gramm/auth/account_logout.html'


class ChangeUserPassword(SignInRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'django_gramm/editing/change_password.html'

    form_class = PasswordEditForm

    def get_success_url(self):
        return reverse_lazy(
            'django_gramm:edit_profile', args=(self.request.user.username,)
        )

    def form_valid(self, form):
        messages.success(self.request, 'Password successfully changed')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error changing password')

        return super().form_invalid(form)


class UserPasswordReset(auth_views.PasswordResetView):
    template_name = 'django_gramm/editing/password_reset_form.html'
    form_class = UserPasswordResetForm
    email_template_name = 'django_gramm/editing/password_reset_email.html'
    success_url = reverse_lazy('django_gramm:password_reset_done')


class UserPasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = 'django_gramm/editing/password_reset_done.html'


class UserPasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = 'django_gramm/editing/password_reset_confirm.html'

    form_class = UserPasswordResetConfirmForm

    success_url = reverse_lazy('django_gramm:password_reset_complete')


class UserPasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name = 'django_gramm/editing/password_reset_complete.html'


class UserEmailVerificationSentView(account_views.EmailVerificationSentView):
    template_name = 'django_gramm/auth/account_verification_sent.html'
