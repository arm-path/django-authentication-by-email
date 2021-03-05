import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.db.models import signals

from .tasks import send_verification_email


class UserAccountManager(BaseUserManager):
    """ Менеджер модели пользователи """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Необходимо указать адрес электронной почты')

        if not password:
            raise ValueError('Необходимо указать пароль')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """ Модель пользователей """
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserAccountManager()

    email = models.EmailField('Электронная почта', unique=True, blank=False, null=False)
    name = models.CharField('Имя', max_length=31, blank=True, null=True)
    surname = models.CharField('Фамилие', max_length=31, blank=True, null=True)
    image = models.ImageField('Фотография', upload_to='users/', blank=True, null=True)
    date_birth = models.DateField('Дата рождения', blank=True, null=True)
    is_staff = models.BooleanField('Статус администратора', default=False)
    verification_uuid = models.UUIDField('Уникальный UUID', default=uuid.uuid4)
    is_active = models.BooleanField('Активно', default=False)

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


def user_post_save(sender, instance, signal, *args, **kwargs):
    """ Подтверждение электронной почты. """
    if not instance.is_active:
        send_verification_email.delay(instance.pk)


signals.post_save.connect(user_post_save, sender=User)
