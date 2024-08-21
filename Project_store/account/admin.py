from django.contrib import admin
from .models import Customer, Address

"""habilitar la administración de los modelos en la interfaz de administración de Django,
 facilitando la gestión de datos relacionados con el modelo de Customer y Adress"""
admin.site.register(Customer)
admin.site.register(Address)