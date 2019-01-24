from .models import List, Item
from rest_framework import serializers

class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('name','user')


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('text', 'date','list')