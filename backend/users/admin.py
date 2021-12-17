from django import forms
from django.conf import settings
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .forms import MyUserChangeForm
from .models import MyUser


@register(MyUser)
class MyUserAdmin(UserAdmin):
  #  form = MyUserChangeForm

    list_display = (
        'username', 'first_name', 'last_name', 'email', 'get_avatar',
    )
    fields = (
        ('username', 'email', ),
        ('first_name', 'last_name', ),
        ('avatar',),
    )
    fieldsets = []

    search_fields = (
        'username', 'email',
    )
    list_filter = (
        'first_name', 'email',
    )
    save_on_top = True
    empty_value_display = settings.EMPTY_VALUE_DISPLAY

    def get_avatar(self, obj):
        if obj.avatar:
            return mark_safe(
                f'<img src={obj.avatar.url} width="50" hieght="50"'
            )

    get_avatar.short_description = 'Изображение'
