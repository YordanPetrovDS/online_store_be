from rest_framework.serializers import Serializer


class EmptySerializer(Serializer):
    """For correct swagger schema processing in case the response is empty"""
