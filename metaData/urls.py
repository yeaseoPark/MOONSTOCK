from django.urls import path

from . import views

app_name = 'metaData'

urlpatterns = [
    path('enditem/', views.endItemIndex, name = 'endItemIndex'),
]