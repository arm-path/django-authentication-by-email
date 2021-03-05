import logging

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template import loader
from django.urls import reverse

from django_settings.celery import app


@app.task
def send_verification_email(user_id):
    """ Отправление письма на указанный email, для активации пользователя """
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        send_mail(
            'Подтвердите свою учетную запись',
            'Перейдите по этой ссылке, чтобы подтвердить свою учетную запись:'
            'http://localhost:8000%s' % reverse('verification', kwargs={'uuid': str(user.verification_uuid)}),
            'arm.path.py@gmail.com',
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)


@app.task
def password_reset_send_mail(subject_template_name, email_template_name, context,
                             from_email, to_email, html_email_template_name):
    """ Отправление письма на указанный email, для сброса пароля """
    UserModel = get_user_model()
    context['user'] = UserModel.objects.get(pk=context['user'])
    subject = loader.render_to_string(subject_template_name, context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')
    email_message.send()
