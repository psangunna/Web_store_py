from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views
                   
app_name='graphs'
                  
urlpatterns = [ 
    path('dashboard/',views.dashboard_graphs, name='dashboard_graphs'),
    path('sales_trend/',views.sales_trend, name='sales_trend'),
    path('product_stock/',views.product_stock, name='product_stock'),
    path('product_perform/',views.product_perform, name='product_perform'),
    path('product_info_per_week/', views.product_info_per_week_view, name='product_info_per_week'),
        ]