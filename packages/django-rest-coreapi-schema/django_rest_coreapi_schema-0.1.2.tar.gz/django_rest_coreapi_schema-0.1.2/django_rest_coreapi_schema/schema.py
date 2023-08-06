from collections import OrderedDict
from rest_framework.schemas.inspectors import AutoSchema
from django_rest_coreapi_schema import utils


class CoreAPIAutoSchema(AutoSchema):

    def get_filter_fields(self, path, method):
        if not self._allows_filters(path, method):
            return []

        fields = []
        for filter_backend in self.view.filter_backends:
            if getattr(self.view, 'filter_fields', None) and self.view.filter_fields:
                serializer_fields = OrderedDict(
                    y for y in filter(
                        lambda x: x[0] in self.view.filter_fields,
                        filter_backend().get_fields().items()
                    )
                )
            else:
                serializer_fields = filter_backend().get_fields()
            fields += utils.coreapi_field_list(serializer_fields)
        return fields

    def get_path_fields(self, path, method):
        view = self.view
        if getattr(view, 'queryset', None):
            if hasattr(view.queryset, '__call__'):
                if getattr(view.queryset(), 'get_fields', None):
                    serializer_fields = view.queryset().get_fields()
                    return utils.coreapi_field_list(serializer_fields, 'path')

        return super(CoreAPIAutoSchema, self).get_path_fields(path, method)
