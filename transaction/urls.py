from django.urls import path

from . import views

app_name = 'transaction'

urlpatterns = [
    # inventory urls
    path('inventory/', views.inventoryIndex, name="inventoryIndex"),
    path('inventory/modify/<int:inv_id>/', views.initialInv_modify, name="initialInv_modify"),
    # buy urls
    path('buy/', views.buyIndex, name="buyIndex"),
    path('buy/add/', views.buy_add, name="buy_add"),
    path('buy/delete/<int:buy_id>', views.buy_delete, name="buy_delete"),

]
