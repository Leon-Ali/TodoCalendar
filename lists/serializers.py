from .models import List, Item
from rest_framework import serializers


class ChoicesField(serializers.Field):
    def __init__(self, choices, **kwargs):
        self._choices = choices
        super(ChoicesField, self).__init__(**kwargs)

    def to_representation(self, obj):
        for i in self._choices:
            if obj in i:
                return i[-1]


    def to_internal_value(self, data):
        for i in self._choices:
            if data in i:
                print(i[0])
                return i[0]




class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('name','user')


class ItemSerializer(serializers.ModelSerializer):
    status = ChoicesField(choices=Item.STATUS_CHOICES)

    class Meta:
        model = Item
        fields = ('text', 'date','list', 'status')