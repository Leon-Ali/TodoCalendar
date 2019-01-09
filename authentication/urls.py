from django.urls import path
from . import views

urlpatterns = [
    path('users', views.SignUp.as_view(), name='signup'),
]