from django.urls import path

from . import views

app_name = 'metaData'

urlpatterns = [
    # EndItem Path
    path('enditem/', views.endItemIndex, name='endItemIndex'),
    path('enditem/add/', views.endItem_add, name='endItem_add'),
    path('enditem/detail/<int:endItem_id>/', views.endItem_detail, name="endItem_detail"),
    path('enditem/modify/<int:endItem_id>/', views.endItem_modify, name="endItem_modify"),
    path('enditem/delete/<int:endItem_id>/', views.endItem_delete, name="endItem_delete"),
    # BOM Path
    path('bom/', views.bomIndex, name='bomIndex'),
    path('bom/add/<int:item_id>/', views.bom_add, name='bom_add'),
    path('bom/detail/<int:bomItem_id>/', views.bom_detail, name="bom_detail"),
    path('bom/modify/<int:bomItem_id>/', views.bom_modify, name="bom_modify"),
    path('bom/delete/<int:bomItem_id>/', views.bom_delete, name="bom_delete"),
    # Vendor Path
    path('otherCompany/vendor/', views.vendorIndex, name='vendorIndex'),
    path('otherCompany/vendor/add/', views.vendor_add, name='vendor_add'),
    path('otherCompany/vendor/detail/<int:vendor_id>/', views.vendor_detail, name='vendor_detail'),
    path('otherCompany/vendor/delete/<int:vendor_id>/', views.vendor_delete, name='vendor_delete'),
    path('otherCompany/vendor/modify/<int:vendor_id>/', views.vendor_modify, name='vendor_modify'),
    # Customer Path
    path('otherCompany/customer/', views.customerIndex, name='customerIndex'),
    path('otherCompany/customer/add/', views.customer_add, name='customer_add'),
    path('otherCompany/customer/detail/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('otherCompany/customer/delete/<int:customer_id>/', views.customer_delete, name='customer_delete'),
    path('otherCompany/customer/modify/<int:customer_id>/', views.customer_modify, name='customer_modify'),
]
