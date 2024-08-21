from django.contrib import admin

from .models import Order, OrderItem
"""habilitar la administración de un modelo específico en la interfaz de administración de Django,
 facilitando la gestión de datos relacionados con los modelos de : Order y OrderItem """ 
admin.site.register(Order)
admin.site.register(OrderItem)