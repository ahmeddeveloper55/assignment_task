import django_filters
from . import models


class TagsField(django_filters.ModelMultipleChoiceFilter):
    """
    This field represents the tags field,
    as it can be used in all filters built through Django Filters framework.
    """

    def __init__(self, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault('field_name', 'tags')
        kwargs.setdefault('to_field_name', 'id')
        kwargs.setdefault('conjoined', False)
        kwargs.setdefault('queryset', models.Tag.activated_objects.all())
        super().__init__(**kwargs)
