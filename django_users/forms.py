from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm

from .models import User
from .tasks import password_reset_send_mail


class RegistrationForm(UserCreationForm):
    """ Форма регистрации пользователя """
    email = forms.EmailField(max_length=150,
                             label="Электронный адрес",
                             widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(max_length=150,
                                label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(max_length=150,
                                label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField(label='Введите текст с картинки')

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class AuthorizationUserForm(AuthenticationForm):
    """Форма авторизации пользователя"""
    username = forms.EmailField(max_length=150,
                                label="Электронная почта",
                                widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password = forms.CharField(max_length=150,
                               label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class PasswordResetSendEmailForm(PasswordResetForm):
    """ Форма сброс пароля, отправление письма на указанный email """
    email = forms.EmailField(
        label="Электронная почта",
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'id': 'email', 'autocomplete': 'email'})
    )
    captcha = CaptchaField(label='Введите текст с картинки')

    def send_mail(self, subject_template_name, email_template_name, context,
                  from_email, to_email, html_email_template_name=None):
        context['user'] = context['user'].id
        password_reset_send_mail.delay(subject_template_name=subject_template_name,
                                       email_template_name=email_template_name,
                                       context=context, from_email=from_email, to_email=to_email,
                                       html_email_template_name=html_email_template_name)


class PasswordResetChangePasswordForm(SetPasswordForm):
    """ Форма изменения пароля """
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='Подтвердите пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'autocomplete': 'new-password'}),
    )
