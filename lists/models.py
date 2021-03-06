from django.db import models
from django.contrib.auth.models import User

class List(models.Model):
    name = models.CharField(max_length=250, default='untitled')
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)


class Item(models.Model):

    SCHEDULED = 'SC'
    INPROGRESS = 'IN'
    COMPLETED = 'CO'

    STATUS_CHOICES = (
        (SCHEDULED, 'scheduled'),
        (INPROGRESS, 'in progress'),
        (COMPLETED, 'completed')
    )

    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=SCHEDULED)


