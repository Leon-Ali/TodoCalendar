from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from lists.serializers import ListSerializer, ItemSerializer
from .models import List, Item


class Lists(generics.ListCreateAPIView):
    """Create the List and get all the Lists"""
    queryset = List.objects.all()
    serializer_class = ListSerializer


class ListDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, Update and Destroy a list by id"""
    queryset = List.objects.all()
    serializer_class = ListSerializer


class Items(APIView):
    """Creates the Item"""

    def post(self, request, pk, format='json'):
        list_ = List.objects.get(id=pk)
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save(list=list_)
            if item:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        list_ = List.objects.get(id=pk)
        items = Item.objects.filter(list=list_).all()
        serializer = ItemSerializer(items, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



