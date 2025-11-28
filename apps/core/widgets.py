from django.db.models import Q
from django.utils.encoding import smart_str
from import_export import widgets
from import_export.widgets import Widget


class ChoicesWidget(Widget):
    """
    A custom widget for handling model fields with choices in Django forms.

    This widget converts between the internal stored value (e.g., integer or string)
    and the human-readable display label of a choice field.

    It supports cleaning input values by matching either the display label or
    the internal value, and renders the display label when exporting data.
    """

    def __init__(self, choices, coerce_to_string=True):
        """
        Initialize the StatusWidget.

        Args:
            choices (list or tuple): Iterable of (value, display_label) tuples representing the choices.
            coerce_to_string (bool): Whether to coerce the output to string (default True).

        Sets up forward and reverse mappings between internal values and display labels.
        """
        super().__init__(coerce_to_string)
        self.choices = dict(choices)  # Map internal values to display strings
        self.reverse_choices = {k for k, v in choices}

    def clean(self, value, row=None, *args, **kwargs):
        """
        Convert input (numeric or display string) to internal choice value.

        Raises ValueError if input is invalid.
        """
        if value is None:
            return None

        value = str(value).strip()

        if value.isdigit() and int(value) in self.choices:
            return int(value)

        if value in self.reverse_choices:
            return value

        raise ValueError(f"Invalid status value: {value}")

    def render(self, value, obj=None):
        """
        Convert internal value (from model) to display string (for export).

        Args:
            value: The internal choice value to render.
            obj: The object instance being exported (optional).

        Returns:
            The human-readable display string for the given internal value.
        """
        return self.choices.get(value, '')


class ManyToManyWidget(widgets.ManyToManyWidget):
    """
    A custom widget for handling many-to-many relationships in Django forms.

    This widget allows for querying and processing model instances based on specified fields.
    It provides methods to clean input values and export data in a specified format.
    """

    def __init__(self, model, fields=None, render_field=None, separator=',', *args, **kwargs):
        """
        Initializes an instance of the class with the specified model and fields.
        """
        # Store the model class in the instance.
        self.model = model

        # Store the fields to be used for querying. Defaults to None if not provided.
        self.fields = fields

        # Store the render field to be used for render field. Defaults to None if not provided.
        self.render_field = render_field

        # Store the render separator to be used for separator field. Defaults to , if not provided.
        self.separator = separator

        # Call the parent class's __init__ method with any additional arguments.
        super().__init__(model, *args, **kwargs)

    def clean(self, value, row=None, *args, **kwargs):
        """
        Cleans and processes the provided value, splitting it by commas, and retrieves objects from the model
        where any of the specified fields match each part of the split value.

        Returns:
            list: A list of objects that match the value in any of the specified fields,
                  with each object being the first match from the queryset.
        """
        query = Q()

        if not value:
            return self.model.objects.none()

        if isinstance(value, (float, int)):
            ids = [int(value)]

        else:
            ids = value.split(self.separator)
            ids = filter(None, [i.strip() for i in ids])

        for val in ids:
            for field in self.fields:
                query |= Q(**{field: val})

        return self.model.objects.filter(query)

    def render(self, value, obj=None):
        """
        Exports a list of objects by joining the values of the specified field with a separator.

        Returns:
            str: A string of field values joined by the specified separator. Returns an empty string if no value is provided.
        """
        # Return an empty string if the input value is not provided or is empty.
        self._obj_deprecation_warning(obj)
        if value is not None:
            values = [smart_str(getattr(obj, self.render_field)) for obj in value.all()]
            return self.separator.join(values)
        return ""
