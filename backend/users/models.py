"""Модуль для создания, настройки и управления пользователями.

Задаёт модели и методы для настроийки и управления пользователями
приложения `Foodgram`. Модель пользователя основана на модели
AbstractUser из Django для переопределения полей обязательных для заполнения.
"""
from api.conf import (MAX_LEN_EMAIL_FIELD, MAX_LEN_USERS_CHARFIELD,
                      MIN_USERNAME_LENGTH)
from django.contrib.auth.models import AbstractUser
from django.db.models import (CharField, CheckConstraint, EmailField,
                              ManyToManyField, Q)
from django.db.models.functions import Length
from django.utils.translation import gettext_lazy as _

CharField.register_lookup(Length)


class MyUser(AbstractUser):
    """Настроенная под приложение `Foodgram` модель пользователя.

    При создании пользователя все поля обязательны для заполнения.

    Attributes:
        email(str):
            Адрес email пользователя.
            Проверка формата производится внутри Dlango.
            Установлено ограничение по максимальной длине.
        username(str):
            Юзернейм пользователя.
            Установлены ограничения по минимальной и максимальной длине.
        first_name(str):
            Реальное имя пользователя.
            Установлено ограничение по максимальной длине.
        last_name(str):
            Реальная фамилия пользователя.
            Установлено ограничение по максимальной длине.
        password(str):
            Пароль для авторизации.
            Внутри Django проходит хэш-функцию с добавлением
            `соли` settings.SECRET_KEY.
            Хранится в зашифрованном виде.
            Установлено ограничение по максимальной длине.
        subscribe(int):
            Ссылки на id связанных пользователей.
    """
    email = EmailField(
        verbose_name='Адрес электронной почты',
        max_length=MAX_LEN_EMAIL_FIELD,
        unique=True,
        help_text=f'Required<={MAX_LEN_EMAIL_FIELD} characters.'
    )
    username = CharField(
        verbose_name='Уникальный юзернейм',
        max_length=MAX_LEN_USERS_CHARFIELD,
        unique=True,
        help_text=(
            f'Required.{MIN_USERNAME_LENGTH}-{MAX_LEN_USERS_CHARFIELD}'
            ' characters.'
        )
    )
    first_name = CharField(
        verbose_name='Имя',
        max_length=MAX_LEN_USERS_CHARFIELD,
        help_text=f'Required<={MAX_LEN_USERS_CHARFIELD} characters.'
    )
    last_name = CharField(
        verbose_name='Фамилия',
        max_length=MAX_LEN_USERS_CHARFIELD,
        help_text=f'Required<={MAX_LEN_USERS_CHARFIELD} characters.'
    )
    password = CharField(
        verbose_name=_('password'),
        max_length=MAX_LEN_USERS_CHARFIELD,
        help_text=f'Required<={MAX_LEN_USERS_CHARFIELD} characters.'
    )
    subscribe = ManyToManyField(
        verbose_name='Подписка',
        related_name='subscribers',
        to='self',
        symmetrical=False,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        constraints = (
            CheckConstraint(
                check=Q(username__length__gte=MIN_USERNAME_LENGTH),
                name='\nusername too short\n',
            ),
        )

    def __str__(self):
        return f'{self.username}: {self.email}'
