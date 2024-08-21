from django.conf import settings
from django.db import models 
from django.urls import reverse
from store.models import Product
from django.utils.translation import gettext_lazy as _ 
from django.db import models, transaction
from django.core.exceptions import ValidationError
from store.number import create_ref_number

"""
    Modelo que representa un pedido realizado por un usuario.
"""
class Order(models.Model):
    ref_no=models.CharField(_("Ref number"),max_length=255, blank = True, null = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    full_name = models.CharField(_('Customer name'),max_length=50,  null=True)
    email=models.CharField(max_length=255,blank=True,  null=True)
    address1 = models.CharField(max_length=250,  null=True)
    address2 = models.CharField(max_length=250, blank=True,  null=True)
    country = models.CharField(max_length=100,  null=True)
    city = models.CharField(max_length=100,  null=True)
    contact_no = models.CharField(_('Contact nº'), max_length=100,  null=True)
    post_code = models.CharField(max_length=20,  null=True)
    created = models.DateTimeField(_("Created at"),auto_now_add=True)
    updated = models.DateTimeField(_("Updated at"),auto_now=True)
    shipping = models.DecimalField(_("Shipping"),max_digits=5, decimal_places=2, null = True, default="11.50")
    total_paid = models.DecimalField(_("Total"),max_digits=6, decimal_places=2, help_text=_("Shipping price included 11.50"),)
    order_key = models.CharField(max_length=200, blank=True,  null=True)
    billing_status = models.BooleanField(_('Paid'),default=False)
    billing_date = models.DateTimeField(_("Billing at"), blank=True, null=True)
    saved_later = models.BooleanField(_("Saved"),default=False, help_text=_("saved order for later"))
    
    class Meta:
        ordering = ('-created',)
    
    def get_absolute_url(self):
        """
        Devuelve la URL absoluta para editar el pedido.
        """
        return reverse('inventory:edit_order', kwargs={'pk': self.pk})
    
    
    def update_total_paid(self):
        """
        Actualiza total_paid basándose en la suma de amount y shipping de OrderItems.
        """
        with transaction.atomic():
            order_items = self.items.all()  # Assuming 'items' is the related_name for OrderItem in Order
            total_amount = sum(order_item.amount for order_item in order_items)
            self.total_paid = total_amount + self.shipping
            self.save()
     
    
    def save(self, *args, **kwargs):
        """
        Método personalizado para generar un número de referencia para la orden si no se ha proporcionado.
        """
        if not self.ref_no:
            
            self.ref_no = create_ref_number('ORD', Order, add_filter = True)
            
           

        super().save(*args, **kwargs) 

    def __str__(self):
        return str(self.id)
       

    


class OrderItem(models.Model):
    """
    Modelo que representa un artículo en un pedido.
    """
    order = models.ForeignKey(Order,  
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.RESTRICT)
    price = models.DecimalField(_('Price €'),max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(_("Quantity(unit)"),default=1)
    amount = models.DecimalField(max_digits=6, decimal_places=2, )
    

    
    '''
    Al guardar una instancia de OrderItem, el método get_amount se llamará automáticamente 
    y el campo de amount se actualizará en consecuencia.
    '''
    def get_amount(self):
        """
        Calcula el importe total para el item del pedido.
        """
        amount = self.price * self.quantity
        return amount



    def update_related_objects(self):
        """
        Actualiza objetos relacionados (por ejemplo, stock del producto) según billing_status.
        """
        with transaction.atomic():

            # Verifica si billing_status es True en el Order asociado
            if self.order.billing_status:
                # Actualiza las cantidades de stock del producto
                product = self.product
                if product.stock_real != None:
                    if self.quantity > product.stock_real:
                        raise ValidationError("Insufficient stock.")
                    product.stock_real -= self.quantity
                else:
                    raise ValidationError("Check the stock of the product and update it")
                
                product.save()

    def save(self, *args, **kwargs):
        """
        Método de guardado personalizado para actualizar el monto antes de guardar.
        """
        self.amount = self.get_amount()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)
      
