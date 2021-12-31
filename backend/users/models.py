from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, CheckConstraint, EmailField, Q
from django.db.models.functions import Length
from django.utils.translation import gettext_lazy as _

CharField.register_lookup(Length)

MIN_USERNAME_LENGTH = 3
IMAGE_EXTENSION = ('jpg', 'png',)
MAX_LEN_CHARFIELD = 150


class MyUser(AbstractUser):
    '''
    Настроенная модель пользователя.
    '''
    email = EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True,
        help_text='Required. <=254 characters.'
    )
    username = CharField(
        verbose_name='Уникальный юзернейм',
        max_length=MAX_LEN_CHARFIELD,
        unique=True,
        help_text=(
            f'Required.{MIN_USERNAME_LENGTH}-{MAX_LEN_CHARFIELD} characters.'
        )
    )
    first_name = CharField(
        verbose_name='Имя',
        max_length=MAX_LEN_CHARFIELD,
        help_text=f'Required.<={MAX_LEN_CHARFIELD} characters.'
    )
    last_name = CharField(
        verbose_name='Фамилия',
        max_length=MAX_LEN_CHARFIELD,
        help_text=f'Required.<={MAX_LEN_CHARFIELD} characters.'
    )
    password = CharField(
        verbose_name=_('password'),
        max_length=MAX_LEN_CHARFIELD,
        help_text=f'Required.<={MAX_LEN_CHARFIELD} characters.'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']
        constraints = (
            CheckConstraint(
                check=Q(username__length__gte=MIN_USERNAME_LENGTH),
                name='\nusername too short\n',
            ),
        )

    def __str__(self):
        return f'{self.username}: {self.email}'
