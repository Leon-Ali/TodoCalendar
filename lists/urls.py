from django.urls import path
from . import views


urlpatterns = [
    path('lists', views.Lists.as_view(), name='lists'),
    path('lists/<int:pk>/',views.ListDetail.as_view(), name='lists_id'),
    path('lists/<int:pk>/items', views.Items.as_view(), name='items'),
    path('lists/<int:pk>/items/<int:item_pk>', views.ItemsDetail.as_view())
]