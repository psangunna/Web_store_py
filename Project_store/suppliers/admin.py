from django.contrib import admin

# Register your models here.
from .models import Supplier,Purchase_invoice, Purchase_invoice_dtl
"""habilitar la administración de los modelos en la interfaz de administración de Django,
 facilitando la gestión de datos relacionados con los modelos de : Supplier, Purchase_invoice y Purchase_invoice_dtl """ 
admin.site.register(Supplier)
admin.site.register(Purchase_invoice)
admin.site.register(Purchase_invoice_dtl)