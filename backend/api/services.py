from django.shortcuts import get_object_or_404

from recipes.models import AmountIngredient

from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from .tuns import ADD_METHODS, DEL_METHODS


def add_del_obj(self, obj_id, meneger, klass, serializer, request=None):
    '''
    This method adds objects "many-to-many".
    '''
    obj = get_object_or_404(klass, id=obj_id)
    serializer = serializer(obj, context={'request': request})
    exist = meneger.filter(id=obj_id).exists()

    if (self.request.method in ADD_METHODS) and not exist:
        meneger.add(obj)
        return Response(serializer.data, status=HTTP_201_CREATED)

    if (self.request.method in DEL_METHODS) and exist:
        meneger.remove(obj)
        return Response(status=HTTP_204_NO_CONTENT)
    return Response(status=HTTP_400_BAD_REQUEST)


def set_amount_ingredients(recipe, ingredients):
    '''
    Записывает ингредиенты вложенные в рецепт.
    '''
    for ingredient in ingredients:
        AmountIngredient.objects.get_or_create(
            recipe=recipe,
            ingredients=ingredient['ingredient'],
            amount=ingredient['amount']
        )


def check_value_validate(value, klass=None):
    '''
    Проверяет корректность переданного значения.
    При необходимости, проверяет существует ли объект с переданным obj_id
    При нахождении объекта создаётся Queryset[],
    для дальнейшей работы возвращается первое (и единственное) значение.
    '''
    if not str(value).isdigit():
        raise ValidationError(
            f'{value} должно содержать цифру'
        )
    if klass:
        obj = klass.objects.filter(id=value)
        if not obj:
            raise ValidationError(
                f'{value} не существует'
            )
        return obj[0]
