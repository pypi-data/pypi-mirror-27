import rest_framework


def coreapi_field_list(serializer_fields, location='query'):
    fields = []
    for field_name, field in serializer_fields.items():
        if isinstance(field, rest_framework.fields.CharField):
            _type = 'string'
        elif isinstance(field, rest_framework.fields.IntegerField):
            _type = 'integer'
        elif isinstance(field, rest_framework.fields.FloatField):
            _type = 'number'
        elif isinstance(field, rest_framework.fields.BooleanField):
            _type = 'boolean'
        elif isinstance(field, rest_framework.fields.ListField):
            _type = 'array'
        elif isinstance(field, rest_framework.fields.ChoiceField):
            _type = 'choice'
        else:
            _type = 'string'
        fields.append(rest_framework.compat.coreapi.Field(
            name=field_name,
            location=location,
            required=field.required,
            type=_type,
            description=field.help_text or '',
            schema=rest_framework.schemas.inspectors.field_to_schema(field)
        ))

    return fields
