from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

# Manager personalizado para el modelo Product
class ProductManager(models.Manager):
    # Filtra los productos que están activos
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)

# Modelo para las categorías de productos
class Category(models.Model):
    ref_no = models.CharField(_("Ref number"),max_length=15, blank = True)
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])
            
    def __str__(self):
        return self.name

# Modelo principal para los productos
class Product(models.Model):
    """
    The Product table contining all product items.
    """
    ref_no = models.CharField(_("Ref number"),max_length=15, blank = True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    name = models.CharField(
        verbose_name=_("name"), 
        max_length=255,
    )    
    description = models.TextField(verbose_name=_("description"), blank=True)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    slug = models.SlugField(max_length=255)
    buy_price=models.DecimalField(
        verbose_name=_("Buy price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 999.99."),
            },
        },
        max_digits=5,
        decimal_places=2,
    )
    sell_price = models.DecimalField(
        verbose_name=_("Regular price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 999.99."),
            },
        },
        max_digits=5,
        decimal_places=2,
    )

    stock_real=models.IntegerField(blank=True, null=True)
    stock_max=models.IntegerField()
    supplier_id=models.ForeignKey("suppliers.Supplier",on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    updated_stock_at = models.DateTimeField(_("Updated Stock at"), blank = True, null = True)
    is_active = models.BooleanField(
        verbose_name=_("Product active"),
        default=True,
    )
    send_stock_notification = models.BooleanField(default=False)   
    objects = models.Manager()
    products = ProductManager()
     
    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])



    def __str__(self):
        return self.name

    
# Signal (señal) para notificar a un administrador cuando cambia el stock de un producto
@receiver(post_save, sender=Product)
def notify_admin_on_stock_change(sender, instance, created,**kwargs):

    try:
        if not created and instance.stock_real <= 0.9 * instance.stock_max:
            # Desconectar la señal temporalmente
            post_save.disconnect(notify_admin_on_stock_change, sender=Product)
            
            # Activar la notificación actualizando un campo
            instance.send_stock_notification = True
            instance.save()
            
             # Reconectar la señal
            post_save.connect(notify_admin_on_stock_change, sender=Product)
    except Exception as e:
        # Capturar y manejar cualquier excepción
       instance.error_message = str(e)