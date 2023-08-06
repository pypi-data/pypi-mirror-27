from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_200_OK
from django_rest_coreapi_schema.views import DocumentedBaseView
from app.serializers import UserSerializer, FilterSerializer, PathSerializer
from app.paginations import LargeResultsSetPagination


class UserListView(DocumentedBaseView):
    filter_backends = [FilterSerializer]
    filter_fields = ('order', 'username')
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        """
        Return a list of all the existing users.

        """
        # query_params = request.query_params
        return Response({}, status=HTTP_200_OK)


class UserView(DocumentedBaseView):
    queryset = PathSerializer
    body_serializer_class = UserSerializer
    pagination_class = LargeResultsSetPagination

    def get(self, request, username):
        """
        Return the user with username

        """
        return Response({
            'username': username,
            'email': 100,
            'address': 11
        })

    def post(self, request, username):
        """
        Create user with username and return user information

        """
        response = {k: v for k, v in request.data.items()}
        response.update({'username': username})
        return Response(response, status=HTTP_201_CREATED)

    def put(self, request, username):
        """
        Update user with username and return user information

        """
        response = {k: v for k, v in request.data.items()}
        response.update({'username': username})
        return Response(response, status=HTTP_201_CREATED)
