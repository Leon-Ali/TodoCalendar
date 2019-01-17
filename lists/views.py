from rest_framework import generics
from rest_framework import status
from lists.serializers import ListSerializer
from .models import List


class List(generics.ListCreateAPIView):
    """Create the List"""
    queryset = List.objects.all()
    serializer_class = ListSerializer


