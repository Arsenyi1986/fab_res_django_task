from collections.abc import Iterable, Sequence
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db.models import BooleanField, DateTimeField
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def serialize_object(object):
    """
    Сериализация объекта в строку.

    Args:
        object: Объект, который требуется сериализовать.

    Returns:
        str: Строковое представление объекта.

    Description:
        Эта функция принимает объект и возвращает его строковое представление. Если объект является
        экземпляром datetime, то он будет преобразован в локальное время и представлен в формате ISO.
        В противном случае, объект будет просто преобразован в строку.
    """
    if isinstance(object, datetime):
        return timezone.localtime(object).isoformat()
    else:
        return str(object)


def get_detail_key(arg):
    """
    Возвращает ключ для детальной информации в ответе.

    Args:
        arg: Аргумент для проверки на наличие множества элементов.

    Returns:
        str: Ключ "detail" или "details" в зависимости от типа аргумента.
    """
    key = "detail"
    if isinstance(arg, Sequence) and not isinstance(arg, str):
        if len(arg) == 1:
            arg = arg[0]
        else:
            key += "s"
    return key


def handle_custom_exception(exception, context):
    """
    Обработчик исключений для кастомной обработки ошибок.

    Args:
        exception: Исключение, которое произошло.
        context: Контекст запроса.

    Returns:
        Response: Ответ с соответствующим статусом и деталями ошибки.
    """
    if isinstance(exception, MultiValueDictKeyError):
        exception = ValidationError(f"Parameter {exception} is required.")
    if isinstance(exception, ValidationError):
        return Response({get_detail_key(exception.messages): exception.messages}, status.HTTP_400_BAD_REQUEST)
    return exception_handler(exception, context)
