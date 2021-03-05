from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegistrationForm, AuthorizationUserForm, PasswordResetSendEmailForm, PasswordResetChangePasswordForm
from .models import User


class RegistrationView(SuccessMessageMixin, CreateView):
    """ Представление регистрации пользователя """
    form_class = RegistrationForm
    template_name = 'django_users/registration_form.html'
    success_url = reverse_lazy('authorization')
    success_message = 'Регистрация прошла успешно, пожалуйста подтвердите электронный адрес почты'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class AuthorizationView(LoginView):
    """ Представление авторизации пользователя """
    form_class = AuthorizationUserForm
    template_name = 'django_users/authorization_form.html'
    success_url = reverse_lazy('system')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context


class PasswordResetSendEmailView(SuccessMessageMixin, PasswordResetView):
    """ Представление отображения формы, воставновления пароля по электронному адресу  """
    form_class = PasswordResetSendEmailForm
    template_name = 'django_users/recovery_password_send_email_form.html'
    success_url = reverse_lazy('authorization')
    success_message = 'Мы отправили вам инструкцию по установке нового пароля на указанный адрес электронной почты ' \
                      'Вы должны получить ее в ближайшее время.Если вы не получили письмо, пожалуйста, убедитесь, ' \
                      'что вы ввели адрес с которым Вы зарегистрировались, и проверьте папку со спамом.'


class PasswordResetChangePassword(SuccessMessageMixin, PasswordResetConfirmView):
    """ Представление отображения формы ввода нового пароля """
    form_class = PasswordResetChangePasswordForm
    template_name = 'django_users/recovery_password_change_password_form.html'
    success_url = reverse_lazy('authorization')
    success_message = 'Пароль успешно изменен!'


class LogoutSystemView(LogoutView):
    template_name = 'django_users/authorization_form.html'


@login_required(login_url=reverse_lazy('authorization'))
def system_and_logout_view(request):
    """ Представление системы, форма выхода из системы"""
    return render(request, 'django_users/system_and_logout_form.html', {'title': 'Система'})


def verification(request, uuid):
    """ Представление подтверждения электронной почты пользователя """
    try:
        user = User.objects.get(verification_uuid=uuid, is_active=False)
    except User.DoesNotExist:
        raise Http404("User does not exist or is already verified")

    user.is_active = True
    user.save()

    return redirect('authorization')
