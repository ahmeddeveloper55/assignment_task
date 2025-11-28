from rest_framework import validators
from rest_framework.exceptions import ValidationError

from ..core import _


class LessThanValidator:
    """
    validator for start and end fields in a Django REST Framework serializer.
    """
    requires_context = True
    message = _("This field must be less than the {fields[1]}.")

    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message or self.message

    def __call__(self, attrs, serializer):
        values = []

        for field_name in self.fields:
            field = serializer.fields[field_name]
            value = attrs.get(field_name, None)

            if value is None and field.required and serializer.instance is not None:
                value = getattr(serializer.instance, field_name)

            if field.required or value is not None:
                values.append(value or 0)

        if len(values) != len(self.fields):
            return True

        if not all(values[i] < values[i + 1] for i in range(len(values) - 1)):
            raise ValidationError({self.fields[0]: self.message.format(fields=self.fields)})


class UniqueTogetherValidator(validators.UniqueTogetherValidator):
    """
    Validator that corresponds to `unique_together = (...)` on a model class.
    Should be applied to the serializer class, not to an individual field.
    """

    def __call__(self, attrs, serializer):
        self.enforce_required_fields(attrs, serializer)
        queryset = self.queryset
        queryset = self.filter_queryset(attrs, queryset, serializer)
        queryset = self.exclude_current_instance(attrs, queryset, serializer.instance)
        checked_values = [
            value for field, value in attrs.items() if field in self.fields
        ]

        if None not in checked_values and validators.qs_exists(queryset):
            raise ValidationError(self.message, code='unique')
