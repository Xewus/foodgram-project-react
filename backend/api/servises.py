from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from .serializers import FavoriteSerializer, Recipe


def add_del_object(self, pk, klass):
    '''
    This method adds objects "many-to-many"
    relationed "User" and "Recipe".
    Should use it with http.methods "GET" and "DELETE".
    The related object necessarily has fields in position:
    Klass(user, recipe).
    '''
    owner = self.request.user
    recipe = get_object_or_404(Recipe, pk=pk)
    serializer = FavoriteSerializer(recipe)

    if self.request.method == 'GET':
        obj, created = klass.objects.get_or_create(
            owner=owner, recipe=recipe
        )
        if created:
            return Response(
                serializer.data, status=HTTP_201_CREATED
            )
        return Response(status=HTTP_400_BAD_REQUEST)

    obj = klass.objects.filter(owner=owner, recipe=recipe)
    if obj:
        obj.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    return Response(status=HTTP_400_BAD_REQUEST)
