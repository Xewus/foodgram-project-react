from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from users.models import MyUser


@register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = (
        'is_active', 'username', 'first_name', 'last_name', 'email',
    )
    fields = (
        ('is_active', ),
        ('username', 'email', ),
        ('first_name', 'last_name', ),
    )
    fieldsets = []

    search_fields = (
        'username', 'email',
    )
    list_filter = (
        'is_active', 'first_name', 'email',
    )
    save_on_top = True
