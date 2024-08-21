from django.urls import path

from . import views

app_name = 'orders'
 
urlpatterns = [
    path('add/', views.add, name='add'),
    path('order_saved/', views.savedOrder_later, name = 'order_saved'),
    path('order_saved_add/<int:pk>/', views.savedOrder_add, name = 'order_saved_add'),
    path('order_saved_delete/<int:pk>/', views.savedOrder_delete, name = 'order_saved_delete'),
    path('shopping_chart/', views.shopping_chart, name='shopping_chart'),
  
]