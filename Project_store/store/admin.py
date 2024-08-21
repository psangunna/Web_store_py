from django.contrib import admin
from .models import (
    Category,
    Product,)


"""habilitar la administración de los modelos en la interfaz de administración de Django,
 facilitando la gestión de datos relacionados con los modelos de : Category y Product """ 

admin.site.register(Category)

admin.site.register(Product)

