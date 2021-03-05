from django.core.validators import validate_email
from django.http import JsonResponse

from django_users.models import User


def check_email(email):
    """ Проверяет корректность электронной почты """
    try:
        validate_email(email)
    except Exception as e:
        return e.messages[0]


def check_email_registration(request):
    """ Проверяет поле email при регистрации """
    if request.GET:
        email = request.GET.get('email')
        if check_email(email):
            return JsonResponse({'error_email': check_email(email)})
        is_email = User.objects.filter(email=email).exists()
        if is_email:
            return JsonResponse({'error_email': 'На этот почтовый адрес уже зарегистрирован пользователь!'})
        else:
            return JsonResponse({'success_email': 'Свободный почтовый адрес!'})


def check_email_authorization(request):
    """ Проверяет поле email при авторизации """
    if request.GET:
        email = request.GET.get('email')
        if check_email(email):
            return JsonResponse({'error_email': check_email(email)})
        is_email = User.objects.filter(email=email).exists()
        if is_email:
            if User.objects.get(email=email).is_active:
                return JsonResponse({'success_email': 'Свободный почтовый адрес!'})
            else:
                return JsonResponse({'error_email': 'Не подтвержденная учетная запись!'})
        else:
            return JsonResponse({'error_email': 'Пользователь с указанной электронной почтой не найден!'})
