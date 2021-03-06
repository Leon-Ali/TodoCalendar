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
    """Creates the and retrieves Items"""


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


class ItemsDetail(APIView):
    """Retrieve, Update and Destroy an item by id"""

    def delete(self, request, **kwargs):
        list_ = List.objects.get(id=kwargs['pk'])
        item = Item.objects.get(id=kwargs['item_pk']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, **kwargs):
        list_ = List.objects.get(id=kwargs['pk'])
        item = Item.objects.get(id=kwargs['item_pk'])
        serializer = ItemSerializer(item)
        if serializer:
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





