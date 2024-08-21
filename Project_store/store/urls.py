from django.urls import path
  
from . import views 
app_name = 'store'

urlpatterns = [
    path('',views.all_products, name='store_home'),
    path('products/', views.products, name ='products'),
    path('<slug:slug>/', views.product_detail, name = 'product_detail'),
    path('shop/<slug:category_slug>/', views.category_list, name = 'category_list'),
    
    ] 