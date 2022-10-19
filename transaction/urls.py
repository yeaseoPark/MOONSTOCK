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
    path('buy/delete/<int:buy_id>/', views.buy_delete, name="buy_delete"),
    path('buy/modify/<int:buy_id>/', views.buy_modify, name="buy_modify"),
    path('buy/detail/<int:buy_id>/', views.buy_detail, name="buy_detail"),

    # sell urls
    path('sell/', views.sellIndex, name="sellIndex"),
    path('sell/add/', views.sell_add, name="sell_add"),
    path('sell/detail/<int:sell_id>/', views.sell_detail, name="sell_detail"),
    path('sell/delete/<int:sell_id>/', views.sell_delete, name="sell_delete"),
    path('sell/modify/<int:sell_id>/', views.sell_modify, name="sell_modify"),

    # produce urls
    path('produce/', views.produceIndex, name="produceIndex"),
    path('produce/add/', views.produce_add, name="produce_add"),
    path('produce/detail/<int:produce_id>/', views.produce_detail, name = "produce_detail")

]
