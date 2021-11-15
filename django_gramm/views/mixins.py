from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy


class SignInRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('django_gramm:login')
