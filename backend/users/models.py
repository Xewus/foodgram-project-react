from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models import (CASCADE, CharField, CheckConstraint, EmailField,
                              ForeignKey, ImageField, Model, Q, URLField)
from django.db.models.functions import Length

CharField.register_lookup(Length)

MIN_USERNAME_LENGTH = 2
IMAGE_EXTENSION = ('jpg', 'png', )
LIMIT_AVATAR_SIZE = 2  # Mb


def size_image_validator(obj):
    limit = LIMIT_AVATAR_SIZE * 1024 * 1024
    if obj.size > limit:
        raise ValidationError(
            f'Размер {obj} больше ограничения {LIMIT_AVATAR_SIZE}'
        )


def path_avatars_upload(obj, file):
    return f'avatars/{obj.pk}/{file}'


class MyUser(AbstractUser):
    '''
    Настроенная моделб пользователя.
    '''
    email = EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True
    )
    username = CharField(
        verbose_name='Уникальный юзернейм',
        max_length=150,
        unique=True
    )
    first_name = CharField(
        verbose_name='Имя',
        max_length=150
    )
    last_name = CharField(
        verbose_name='Фамилия',
        max_length=150
    )
    avatar = ImageField(
        verbose_name='Аватар',
        upload_to=path_avatars_upload,
        blank=True,
        null=True,
        validators=(
            FileExtensionValidator(
                allowed_extensions=(IMAGE_EXTENSION),
                message=(f'Allowed only {IMAGE_EXTENSION}')
            ),
            size_image_validator,
        )
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']
        constraints = (
            CheckConstraint(
                check=Q(username__length__gt=MIN_USERNAME_LENGTH),
                name='\nusername too short\n',
            ),
        )

    def __str__(self):
        return f'{self.username}: {self.email}'


class SocialLink(Model):
    '''
    Ссылки на профили в соцсетях.
    '''
    owner = ForeignKey(
        verbose_name='Пользователь',
        to=MyUser,
        on_delete=CASCADE,
        related_name='social'
    )
    link = URLField(
        verbose_name='Профиль в соцсети',
        max_length=150,
        unique=True
    )

    class Meta:
        verbose_name = 'Профиль в соцсети'
        verbose_name_plural = 'ТПрофили в соцсетях'
        ordering = ('owner', 'link', )
