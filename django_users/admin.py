from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import Group

from django_users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email',)
    ordering = ('-is_active', 'email')
    fieldsets = (
        ('Основная информация',
         {'fields': (('email', 'is_active'), 'password', 'name', 'surname', 'image', 'date_birth')}),
        ('Права пользователя',
         {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions', 'verification_uuid')}),
        ('Прочая информация', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),
    )
    readonly_fields = ('verification_uuid', )


class ProxyGroups(Group):
    class Meta:
        proxy = True
        verbose_name = Group._meta.verbose_name
        verbose_name_plural = Group._meta.verbose_name_plural


admin.site.register(ProxyGroups)

admin.site.site_header = "Администрирование сайта"
admin.site.site_title = "Администрирование сайта"
