from .models import List
from rest_framework import serializers

class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('name',)