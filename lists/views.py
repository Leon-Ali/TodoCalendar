from rest_framework import generics
from rest_framework import status
from lists.serializers import ListSerializer
from .models import List


class Lists(generics.ListCreateAPIView):
    """Create the List and get all the Lists"""
    queryset = List.objects.all()
    serializer_class = ListSerializer


class ListDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, Update and Destroy a list by id"""
    queryset = List.objects.all()
    serializer_class = ListSerializer


