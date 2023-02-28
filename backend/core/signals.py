from pathlib import Path

from django.db.models.signals import post_delete
from django.dispatch import receiver
from recipes.models import Recipe


@receiver(post_delete, sender=Recipe)
def delete_image(sender: Recipe, instance: Recipe, *a, **kw) -> None:
    """Удаляет картинку при удаление рецепта. Привет Андрею Пронину.

    Args:
        sender (Recipe): Модель отправляющая сигнал.
        instance (Recipe): Удалённый рецепт.
    """
    image = Path(instance.image.path)
    if image.exists():
        image.unlink()
