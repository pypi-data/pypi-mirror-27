import collections
from rest_framework import serializers
from rest_framework.utils import html


class ListField(serializers.ListField):
    def to_internal_value(self, data):
        """
        List of dicts of native values <- List of dicts of primitive datatypes.
        """
        _data = data[0].split(',') if len(data) > 0 else data
        if html.is_html_input(_data):
            data = html.parse_html_list(_data)
        if isinstance(_data, type('')) or isinstance(_data, collections.Mapping) or not hasattr(data, '__iter__'):
            self.fail('not_a_list', input_type=type(_data).__name__)
        if not self.allow_empty and len(_data) == 0:
            self.fail('empty')
        return [self.child.run_validation(item) for item in _data]