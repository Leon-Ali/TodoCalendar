from django.db import models

class List(models.Model):
    name = models.CharField(max_length=250, default='untitled')


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
    date = models.DateField()


