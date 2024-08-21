from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from store.models import Product

# Importa la clase Basket del archivo basket.py en el mismo directorio
from .basket import Basket
 
def basket_summary(request):
    # Obtiene la instancia del cesta de compras a partir de la solicitud
    basket = Basket(request)
    
    # Renderiza la página de resumen del cesta con el cesta como parte del contexto
    return render(request, 'basket/summary.html', {'basket': basket})


def basket_add(request):
    # Obtiene la instancia del cesta de compras a partir de la solicitud
    basket = Basket(request)
    
    # Verifica si la solicitud es de tipo POST
    if request.POST.get('action') == 'post':
        # Obtiene el ID y la cantidad del producto seleccionado desde la solicitud POST
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
       
        # Obtiene el objeto Product correspondiente al ID
        product = get_object_or_404(Product, id=product_id)
        
        # Agrega el producto al cesta con la cantidad especificada
        basket.add(product=product, qty=product_qty)

        # Obtiene la cantidad actualizada de elementos en el cesta
        basketqty = basket.__len__()

        # Devuelve la cantidad actualizada como respuesta JSON
        response = JsonResponse({'qty': basketqty})
        return response

       


def basket_delete(request):
    # Obtiene la instancia del cesta de compras a partir de la solicitud
    basket = Basket(request)
    
    # Verifica si la solicitud es de tipo POST
    if request.POST.get('action') == 'post':
        # Obtiene el ID del producto a eliminar desde la solicitud POST
        product_id = int(request.POST.get('productid'))
        
        # Elimina el producto del cesta
        basket.delete(product=product_id)
        
        # Obtiene la cantidad actualizada de elementos y el subtotal del cesta
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        
        # Devuelve la cantidad actualizada y el subtotal como respuesta JSON
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response
       

def basket_update(request):
    # Obtiene la instancia de la cesta de compras a partir de la solicitud
    basket = Basket(request)
    
    # Verifica si la solicitud es de tipo POST
    if request.POST.get('action') == 'post':
        # Obtiene el ID y la nueva cantidad del producto desde la solicitud POST
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        
        # Actualiza la cantidad del producto en el cesta
        basket.update(product=product_id, qty=product_qty)
  
        # Obtiene la cantidad actualizada de elementos y el subtotal del cesta
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        
        # Devuelve la cantidad actualizada y el subtotal como respuesta JSON
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})

        return response