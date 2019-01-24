from django.db import models
from django.contrib.auth.models import User

class List(models.Model):
    name = models.CharField(max_length=250, default='untitled')
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
    date = models.DateField()


