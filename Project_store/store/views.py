from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from .models import Product, Category

def products(request):
    # Obtener la consulta de búsqueda del parámetro de la URL
    query = request.GET.get('query', '')

    # Filtrar: Usando ProductManager para obtener el conjunto de consultas filtrado
    items = Product.products.all()

    # Aplicar filtro de búsqueda si se proporciona una consulta
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Verificar si no hay elementos coincidentes
    if not items.exists():
        messages.info(request, 'No products match your search.')

    return render(request, 'store/items.html', {
        'products': items,
        'query': query,
    })

def all_products(request):
    # Obtener todos los productos usando ProductManager
    products = Product.products.all()  
    return render(request, 'store/index.html', {'products': products})

def product_detail(request, slug):
    # Obtener un producto específico por su slug
    product = get_object_or_404(Product, slug=slug, is_active=True)

    # Obtener productos relacionados en la misma categoría (excluyendo el producto actual)
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[0:3]

    return render(request, 'store/single.html', {'product': product, 'related_products': related_products})

def category_list(request, category_slug=None):
    # Obtener una categoría específica por su slug
    category = get_object_or_404(Category, slug=category_slug)

    # Obtener productos en la categoría específica
    products = Product.objects.filter(category=category, is_active=True)

    return render(request, 'store/category.html', {'category': category, 'products': products})






