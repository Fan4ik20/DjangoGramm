from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm,
    UserChangeForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
)

from allauth.account.forms import LoginForm, SignupForm

from django_gramm.models import User, Post, Photo, Comment


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = 'username', 'email', 'password1', 'password2'


class AccountRegistrationForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'] = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )

        self.fields['email'] = forms.EmailField(
            widget=forms.EmailInput(attrs={'class': 'form-control'})
        )

        self.fields['password1'] = forms.CharField(
            label='Password',
            widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )

        self.fields['password2'] = forms.CharField(
            label='Password confirmation',
            widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class AccountUserLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['login'] = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )

        self.fields['password'] = forms.CharField(
            widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )

        self.fields['remember'] = forms.CharField(
            required=False,
            widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
        )

        self.order_fields(('login', 'password', 'remember'))


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = 'picture', 'username', 'password', 'email', 'description'

        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'password': forms.PasswordInput(
                attrs={'class': 'form-control'}
            ),

            'email': forms.EmailInput(
                attrs={'class': 'form-control'}
            ),

            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),

            'picture': forms.ClearableFileInput(
                attrs={'class': 'btn btn-primary btn-block'}
            )
        }


class PasswordEditForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    new_password2 = forms.CharField(
        label='New password confirmation',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = 'post_image',
        widgets = {'post_image': forms.ClearableFileInput(
            attrs={'class': 'btn btn-primary btn-block'}
        )}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = 'description',

        widgets = {
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            )
        }


class UserPasswordResetForm(PasswordResetForm):
    class Meta:
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'form-control'}
            )
        }


class UserPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    new_password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = 'content',

        widgets = {'content': forms.TextInput(
            attrs={'class': 'form-control', 'rows': 3}
        )}

        labels = {'content': ''}
