from django.urls import path
from . import views


urlpatterns = [
    path('lists', views.List.as_view(), name='lists'),
]