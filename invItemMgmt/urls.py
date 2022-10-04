from django.urls import path

from . import views

app_name = 'invItemMgmt'

urlpatterns = [
    path('', views.Index, name = 'inventoryIndex'),
]