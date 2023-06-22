"""Модуль содержит дополнительные классы
для настройки основных классов приложения.
"""
from django.db.models import Model, Q
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)


class AddDelViewMixin:
    """
    Добавляет во Viewset дополнительные методы.

    Содержит методы для добавления или удаления объекта связи
    Many-to-Many между моделями.
    Требует определения атрибутов `add_serializer` и `link_model`.

    Example:
        class ExampleViewSet(ModelViewSet, AddDelViewMixin)
            ...
            add_serializer = ExamplSerializer
            link_model = M2M_Model
    """

    add_serializer: ModelSerializer | None = None
    link_model: Model | None = None

    def _create_relation(self, obj_id: int | str) -> Response:
        """Добавляет связь M2M между объектами.

        Args:
            obj_id (int | str):
                `id` объекта, с которым требуется создать связь.

        Returns:
            Responce: Статус подтверждающий/отклоняющий действие.
        """
        obj = get_object_or_404(self.queryset, pk=obj_id)
        try:
            self.link_model(None, obj.pk, self.request.user.pk).save()
        except IntegrityError:
            return Response(
                {"error": "Действие выполнено ранее."},
                status=HTTP_400_BAD_REQUEST,
            )

        serializer: ModelSerializer = self.add_serializer(obj)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def _delete_relation(self, q: Q) -> Response:
        """Удаляет связь M2M между объектами.

        Args:
            q (Q):
                Условие фильтрации объектов.

        Returns:
            Responce: Статус подтверждающий/отклоняющий действие.
        """
        deleted, _ = (
            self.link_model.objects.filter(q & Q(user=self.request.user))
            .first()
            .delete()
        )
        if not deleted:
            return Response(
                {"error": f"{self.link_model.__name__} не существует"},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response(status=HTTP_204_NO_CONTENT)
