from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)

from . import tuns as t


class AddDelViewMixin:
    """
    Миксин для добавления и удаления связанных объектов.
    """
    add_serializer = None

    def add_del_obj(self, obj_id, meneger):
        """
        Добавляет или удаляет связь через "user.many-to-many".
        """
        if not self.add_serializer:
            raise AttributeError

        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)

        menegers = {
            t.SUBSCRIBE_M2M: user.subscribe,
            t.FAVORITE_M2M: user.favorites,
            t.SHOP_CART_M2M: user.carts,

        }
        meneger = menegers[meneger]

        obj = get_object_or_404(self.queryset, id=obj_id)
        serializer = self.add_serializer(
            obj, context={'request': self.request}
        )
        exist = meneger.filter(id=obj_id).exists()

        if (self.request.method in t.ADD_METHODS) and not exist:
            meneger.add(obj)
            return Response(serializer.data, status=HTTP_201_CREATED)

        if (self.request.method in t.DEL_METHODS) and exist:
            meneger.remove(obj)
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)
