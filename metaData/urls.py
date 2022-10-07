from django.urls import path

from . import views

app_name = 'metaData'

urlpatterns = [
    # EndItem Path
    path('enditem/', views.endItemIndex, name = 'endItemIndex'),
    path('enditem/add/', views.endItem_add, name = 'endItem_add'),
    path('enditem/detail/<int:endItem_id>/', views.endItem_detail, name = "endItem_detail"),
    path('enditem/modify/<int:endItem_id>/', views.endItem_modify, name = "endItem_modify"),
    path('enditem/delete/<int:endItem_id>/', views.endItem_delete, name = "endItem_delete"),
    # BOM Path
    path('bom/', views.bomIndex, name = 'bomIndex'),

]