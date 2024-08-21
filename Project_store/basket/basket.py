from decimal import Decimal

from django.conf import settings
 
from store.models import Product
"""La siguiente clase proporciona métodos para agregar, actualizar, eliminar y 
obtener información sobre los productos en la cesta de compras, así como métodos 
para calcular el subtotal y el total del carrito.También tiene métodos para limpiar y guardar el carrito."""

class Basket():
   

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, qty, id_order=None):
        """Agrega un producto al carrito de compras con la cantidad especificada.
        Si el producto ya está en el carrito, actualiza la cantidad."""
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.sell_price), 'qty': qty}
            
        self.save()    

    def __iter__(self):
        """ Recupera los productos correspondientes a los identificadores almacenados en el carrito.
        Asigna los productos a los elementos del carrito y devuelve un generador que produce diccionarios con información del producto en el carrito."""
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
           
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        """Retorna la cantidad total de productos en el carrito.
        Utiliza la función sum para sumar las cantidades de todos los productos en el carrito."""
        return sum(item['qty'] for item in self.basket.values())

    def update(self, product, qty, ):
        """Actualiza la cantidad de un producto en el carrito."""
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty


        self.save()

    def get_subtotal_price(self):
        """Retorna el subtotal del carrito, que es la suma de los precios de cada producto multiplicado por su cantidad."""
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def get_total_price(self):
        """Retorna el precio total del carrito, 
        que es el subtotal más el costo de envío fijo."""

        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(11.50)

        total = subtotal + Decimal(shipping)
      
        return total

    def delete(self, product):
        """Elimina un producto específico del carrito."""
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def clear(self):
        """Elimina completamente el carrito de compras vaciando la sesión"""
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True


