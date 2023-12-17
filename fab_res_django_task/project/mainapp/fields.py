from rest_framework import serializers
from timezone_field import TimeZoneField
from timezone_field.choices import with_gmt_offset


class ClientFilterSerializerField(serializers.JSONField):
    """
    Сериализатор для поля фильтра клиента.
    """
    pass


class TimeZoneSerializerField(serializers.ChoiceField):
    """
    Сериализатор для поля выбора часового пояса.

    Инициализируется с использованием часовых поясов с учетом GMT-смещения (GMT offset).
    """

    def __init__(self, **kwargs):
        super().__init__(
            with_gmt_offset(map(str, TimeZoneField.default_zoneinfo_tzs)), **kwargs
        )

    def to_representation(self, value):
        """
        Преобразует значение часового пояса в строку.

        Args:
            value: Значение часового пояса.

        Returns:
            str: Строковое представление часового пояса.
        """
        return str(super().to_representation(value))
