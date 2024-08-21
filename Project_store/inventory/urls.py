from django.urls import path
from . import views
                   
app_name='inventory'
                  
urlpatterns = [ 
    path('dashboard/',views.inventory, name='inventory'),
    #Products
    path('products/', views.products, name='products'),
    path('products/create_product/', views.create_or_update_product, name='create_product'),
    path('products/update_product/<int:pk>/', views.create_or_update_product, name='update_product'),
    path('products/delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('categories/', views.categories, name='categories'),
    path('categories/category/<int:pk>', views.update_category, name='update_category'),
    path('categories/delete_category/<int:pk>', views.delete_category, name='delete_category'),
    #orders
    path('orders/', views.orders, name='orders'),
    path('orders/create_order/', views.create_or_update_order, name='create_order'),
    path('orders/update_order/<int:pk>/', views.create_or_update_order, name='update_order'),
    path('orders/delete_order/<int:pk>/', views.delete_order, name='delete_order'),
    #account
    path('accounts/', views.accounts, name='accounts'),
    path('accounts/create_account/', views.create_account, name='create_account'),
    path('accounts/update_account/<int:pk>/', views.update_account, name='update_account'),
    path('accounts/delete_account/<int:pk>/', views.delete_account, name='delete_account'),
    #Adresses
    path('accounts/addresses/<int:pk>/', views.create_or_update_addresses, name='addresses'),
    
    # #Supplier
    path('suppliers/', views.suppliers, name='suppliers'),
    path('suppliers/create_supplier/', views.create_or_update_supplier, name='create_supplier'),
    path('suppliers/update_supplier/<int:pk>/', views.create_or_update_supplier, name='update_supplier'),
    path('suppliers/delete_supplier/<int:pk>/', views.delete_supplier, name='delete_supplier'),  
    ###Invoices
    path('invoices/', views.invoices, name='invoices'),
    path('invoices/delete_invoice/<int:pk>/', views.delete_invoice, name='delete_invoice'),
    path('invoices/create_invoice/', views.create_or_update_invoice, name='create_invoice'),
    path('invoices/update_invoice/<int:pk>/', views.create_or_update_invoice, name='update_invoice'),
   
    #inventory  
    path('check_stock_notification/', views.check_stock_notification, name='check_stock_notification'),
    path('get_product_price/<int:product_id>/', views.get_product_price, name='get_product_price'),                        
    path('get_supplier_products/<int:supplier_id>/', views.get_supplier_products, name='get_supplier_products'),
    path('get_address_details/<int:user_id>/', views.get_address_details, name='get_address_details'),
   

    ]      
