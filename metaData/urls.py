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
    # material Path
    path('material/', views.materialIndex, name='materialIndex'),
    path('material/add/', views.material_add, name='material_add'),
    path('material/detail/<int:material_id>/', views.material_detail, name="material_detail"),
    path('material/modify/<int:material_id>/', views.material_modify, name="material_modify"),
    path('material/delete/<int:material_id>/', views.material_delete, name="material_delete"),
    # BOM Path
    path('bom/', views.bomIndex, name='bomIndex'),
    path('bom/add/<int:node_id>/', views.bom_add, name='bom_add'),
    path('bom/delete/<int:node_id>/', views.bom_delete, name='bom_delete'),
    path('bom/update/<int:node_id>/', views.bom_update, name='bom_update'),

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
