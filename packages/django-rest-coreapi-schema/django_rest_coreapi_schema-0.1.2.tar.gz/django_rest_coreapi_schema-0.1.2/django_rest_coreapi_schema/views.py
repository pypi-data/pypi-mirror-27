from rest_framework.views import APIView


class DocumentedBaseView(APIView):
    def get_serializer(self):
        if getattr(self, 'body_serializer_class', None):
            return self.body_serializer_class()

    def get_filter_serializer(self):
        if getattr(self, 'filter_serializer_class', None):
            return self.filter_serializer_class()
