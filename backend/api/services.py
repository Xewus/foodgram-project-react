from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (BasePermission,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from .tuns import ADD_METHODS, DEL_METHODS


class AuthorStaffOrReadOnly(IsAuthenticatedOrReadOnly):
    '''
    Разрешение на создание и изменение только для админов и автора.
    Остальным только чтение объекта.
    '''
    def has_object_permission(self, request, view, obj):
        return (
            request.method in ('GET',)
            or (request.user == obj.author)
            or request.user.is_moderator
            or request.user.is_admin
        )


class AdminOrReadOnly(BasePermission):
    '''
    Разрешение на создание и изменение только для админов.
    Остальным только чтение объекта.
    '''
    def has_permission(self, request, view):
        return (
            request.method in ('GET',)
            or request.user.is_authenticated
            and request.user.is_admin
        )


class PageLimitPagination(PageNumberPagination):
    '''
    Стандартный пагинатор.
    Переименовано имя параметра под требования фронтенда.
    '''
    page_size_query_param = 'limit'


def add_del_obj(self, id, meneger, klass, serializer, request=None):
    '''
    This method adds objects "many-to-many".
    '''
    obj = get_object_or_404(klass, id=id)
    serializer = serializer(obj, context={'request': request})
    exist = meneger.filter(id=id).exists()

    if (self.request.method in ADD_METHODS) and not exist:
        meneger.add(obj)
        return Response(serializer.data, status=HTTP_201_CREATED)

    if (self.request.method in DEL_METHODS) and exist:
        meneger.remove(obj)
        return Response(status=HTTP_204_NO_CONTENT)
    return Response(status=HTTP_400_BAD_REQUEST)
