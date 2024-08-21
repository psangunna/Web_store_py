from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models, transaction
from datetime import datetime

class SupplierManager(models.Manager):
    # Filtra los proveedores que están activos
    def get_queryset(self):
        return super(SupplierManager, self).get_queryset().filter(is_active=True)
               
# Create your models here.
class Supplier(models.Model):
    name=models.CharField(_("Supplier"),max_length=255)
    ref_no=models.CharField(_("Ref number"),max_length=255, blank = True)
    address=models.CharField(max_length=255)
    contact_no=models.CharField(_("Contact number"),max_length=255)
    email=models.CharField(max_length=255)
    description=models.CharField(max_length=255,null = True, blank = True)
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(_("Created by"), max_length=15, null = True, blank = True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)   
    objects=models.Manager()
    supplier = SupplierManager()
          
    class Meta: 
        verbose_name_plural = "Suppliers"# Especifica el nombre en plural en la interfaz de administración
        ordering = ('-created_at',)# Ordena por fecha de creación descendente
    
    def __str__(self):
        return str(self.name)  

      
class Purchase_invoice(models.Model):
    ref_no = models.CharField(_("Ref number"),max_length=15, blank = True)
    inv_date = models.DateTimeField(_("Invoice date"),default=timezone.now)
    supplier = models.ForeignKey(Supplier, on_delete=models.RESTRICT)
    observations = models.CharField(max_length = 4000, blank = True)
    created_by = models.CharField(_("Created by"), max_length=15, null = True, blank = True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    paid_at = models.DateTimeField(_("Paid date"),null=True, blank = True) 
    tax = models.DecimalField(_('Tax'),max_digits=5, decimal_places=2, default="0.00",blank=True)
    discount = models.DecimalField(_('Discount'),max_digits=5, decimal_places=2, blank=True, default="0.00")
    total = models.DecimalField(_("Total"),max_digits=6, decimal_places=2,null=True )
    total_paid = models.DecimalField(_("Paid"),max_digits=6, decimal_places=2,null=True, blank = True, default="0.00")
    to_paid = models.DecimalField(_("To Paid"),max_digits=6, decimal_places=2,null=True, blank = True,default="0.00")
    is_paid = models.BooleanField(_("Paid"),default=False) 
    is_cancelled = models.BooleanField(_("Cancelled"),help_text=_("Deleted invoices"), default=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    updated_by = models.CharField(_("Updated by"),max_length=15,  null = True, blank = True)
    
    def update_total_paid(self):
        """
        Actualiza el total_pagado basándose en la suma del importe y envío de Purchase_invoice_dtl.
        """
        with transaction.atomic():
            if self.is_paid == True:
                 # Actualiza totales
                self.paid_at = datetime.now()
                self.total_paid = self.total
                self.to_paid = 0

            invoice_items = self.items.all()  #'items' es el related_name para Purchase_invoice_dtl
            total_amount = sum(invoice_item.amount for invoice_item in invoice_items)
            self.total = total_amount + self.tax - self.discount

            self.save()    
 
            
    def __str__(self):
        return str(self.id)
       
              
    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Purchase_invoice'
        db_table ='Purchase_invoice'
            
  
class Purchase_invoice_dtl(models.Model):
    invoice = models.ForeignKey(Purchase_invoice,related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey('store.Product',related_name='invoice_items',
                              on_delete=models.RESTRICT) 
    qty = models.PositiveBigIntegerField(_("Quantity(unit)"), default="1") 
    price = models.DecimalField(max_digits=5, decimal_places=2, )
    amount = models.DecimalField(max_digits=6, decimal_places=2,)

    def update_related_objects(self):
        """
        Actualiza objetos relacionados (por ejemplo, el stock de productos) basándose en billing_status.
        """
        with transaction.atomic():

           # Verifica si billing_status es True en la Order asociada
            
            if self.invoice.is_paid:
                # Actualiza las cantidades de stock del producto
                product = self.product
                if  product.stock_real != None:
                    product.stock_real += self.qty
                else:
                    product.stock_real = self.qty
                product.updated_stock_at = datetime.now()
                product.save()    
                     
    def __str__(self):
        return str(self.id)
     
    class Meta:  
        verbose_name_plural = "Purchase_invoice_dlt"
        db_table = "Purchase_invoice_dlt"
    
 
     
