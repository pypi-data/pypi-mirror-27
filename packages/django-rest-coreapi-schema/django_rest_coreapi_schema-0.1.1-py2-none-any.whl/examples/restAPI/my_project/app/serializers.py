from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    email = serializers.CharField(
        required=False,
        help_text="User email")
    address = serializers.CharField(
        required=False,
        help_text="User address")


class FilterSerializer(serializers.Serializer):
    order = serializers.ChoiceField(
        required=False,
        choices=[("asc", "Asc"), ("desc", "desc")],
        help_text="Order")
    username = serializers.CharField(
        required=False,
        help_text="Username pattern")


class PathSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        help_text="Username")