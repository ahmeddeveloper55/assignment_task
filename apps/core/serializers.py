from django.http import QueryDict
from modeltranslation.fields import TranslationField

from rest_framework import serializers
from rest_framework.fields import SkipField


class Serializer(serializers.Serializer):

    def set_source_attrs(self, field_name, source):
        field = self.fields.get(field_name, None)

        if field is None:
            return

        field.source_attrs = source.split('.')

    def get_field_value(self, filed_name):
        field = self.fields.get(filed_name, None)
        initial_data = getattr(self, 'initial_data', None)

        if field is None:
            return

        if isinstance(field, serializers.HiddenField):
            return field.get_default()

        try:
            if isinstance(initial_data, QueryDict):
                primitive_value = field.get_value(initial_data)
                if primitive_value:
                    return field.run_validation(primitive_value)
        except (SkipField,):
            pass

        return getattr(self.instance, filed_name, None)

    def get_method_action(self):
        method = self.context.get('view', None)
        return getattr(method, 'action', 'null')

    def is_post_action(self):
        action = self.get_method_action()
        return action in ['create']

    def is_put_action(self):
        action = self.get_method_action()
        return action in ['update', 'partial_update']

    def is_safe_method(self):
        return not bool(self.is_post_action() or self.is_put_action())

    def set_meta_attr(self, attr, value):
        meta = getattr(self, 'Meta', None)

        if meta is None:
            return

        setattr(meta, attr, value)


class FormSerializer(Serializer):
    form_class = None

    form = None

    def get_form_class(self, attrs):
        return self.form_class(data=attrs)

    def validate(self, attrs):
        self.form = self.get_form_class(attrs=attrs)
        if not self.form.is_valid():
            raise serializers.ValidationError(self.form.errors)
        return attrs

    def create(self, validated_data):
        return self.form.save()


class ModelSerializer(Serializer, serializers.ModelSerializer):

    def update(self, instance, validated_data):
        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates, we already
        # have an instance pk for the relationships to be associated with.

        fields = self.get_fields()

        for key, field in fields.items():
            if isinstance(field, (serializers.FileField, serializers.ImageField)):
                field = validated_data.get(key, None)
                if not field:
                    validated_data.pop(key, None)

        return super(ModelSerializer, self).update(instance, validated_data)


class TranslationModelSerializer(ModelSerializer):

    def get_fields(self):
        """
        Return the dict of field names -> field instances that should be
        used for `self.fields` when instantiating the serializer.
        """

        fields = super(TranslationModelSerializer, self).get_fields()

        for f in getattr(self, 'Meta').model._meta.fields:
            if f.name in fields and isinstance(f, TranslationField):
                translated_field = f.translated_field
                allow_null = translated_field.null
                allow_blank = translated_field.blank
                fields[translated_field.name].read_only = True
                fields[f.name].required = not (allow_null or allow_blank)
                fields[f.name].allow_null = allow_null
                fields[f.name].allow_blank = allow_blank

        return fields


class ImportSerializer(serializers.Serializer):
    import_file = serializers.FileField()
    format = serializers.ChoiceField(choices=[('csv', 'CSV'), ('xlsx', 'XLSX')], default='xlsx')
