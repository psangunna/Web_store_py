from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.models import Customer, Address
from account.forms import UserAddressForm
from .decorators import superuser_only, staff_user
from store.models import Product, Category
from orders.models import Order, OrderItem
from suppliers.models import Supplier
from .form import ProductForm, OrderForm,AccountFormCreate, AccountFormUpdate,CategoryForm
from suppliers.models import Purchase_invoice, Purchase_invoice_dtl
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from orders.forms import OrderForm, OrderItemForm
from suppliers.form import SupplierForm, PurchaseInvoiceDtlForms, PurchaseInvoiceForm
from datetime import datetime
from .inventory_management import InventoryManager
import json
from store.number import create_ref_number
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def get_dashboard_data():
    """
    Obtiene datos para el panel de control, 
    incluyendo recuentos de cuentas, productos, pedidos y proveedores.
    """
    products = Product.products.all()
    product_count = products.count()
    accounts = Customer.objects.filter(is_active=True)
    account_count = accounts.count()
    orders = Order.objects.all()
    order_count = orders.count() 
    suppliers = Supplier.supplier.all()
    supplier_count = suppliers.count()

    data = {
        'account_count': account_count,
        'product_count': product_count,
        'order_count': order_count,
        'supplier_count':supplier_count,
    }


    return data


@login_required    
@staff_user
def inventory(request):
    """
    Vista para la sección de inventario del panel de control.
    """
    products = Product.products.all()
    dashboard_data = get_dashboard_data()
    inventory_data = InventoryManager.get_inventory_data(products)
    
    product_ids = [product.id for product in products]



    context = {
        'products': products,
        'product_ids_json': json.dumps(product_ids),
        'inventory_data': inventory_data,
         **dashboard_data, # El doble asterisco (**) se usa para desempaquetar los valores de un diccionario.
        }
    
        



    return render(request, 'inventory/dashboard/inventory.html',context)  

#####-----------Products----------------#####
@login_required    
@staff_user
def products(request):
    """
    Vista para la gestión de productos, incluida la creación de nuevas categorías.
    """
    product = Product.objects.all()
    dashboard_data = get_dashboard_data()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            cattype = "CAT"  
            cateNumber = create_ref_number(cattype, Category )
            form.ref_no = cateNumber 
            form.save()
            messages.success(request,'Category has been created')
            return redirect('inventory:products')

    else:
        form = CategoryForm()



    context = {
        'products': product,
        'form': form,
        **dashboard_data  # El doble asterisco (**) se usa para desempaquetar los valores de un diccionario.
    }
    return render(request, 'inventory/dashboard/product_list.html', context)


def create_or_update_product(request, pk=None):
    """
    Vista para la creación o actualización de productos en el inventario.
    """
    prod_number=None
    if pk is not None:
        product = get_object_or_404(Product, pk=pk)
    else:
        product = None
        prodtype = "PRD"
        prod_number = create_ref_number(prodtype, Product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form = form.save(commit=False)
            if pk == None:
                form.ref_no = prod_number

            form.save()
            
            item_name = form.ref_no
            if pk != None:
                messages.success(request, f'Product {item_name} has been updated')
        
            else:
                messages.success(request, f'Product {item_name} has been created')
            return redirect('inventory:products')  # Replace 'store:product_list' with the actual URL name for your product list view
    else:
        form = ProductForm(instance=product)

    return render(request, 'inventory/dashboard/product.html', {'form': form, 'product': product, 'prod_number':prod_number})
  
def delete_product(request, pk):
    """
    Elimina un producto del inventario.
    """
    item = Product.objects.get(id=pk)
    item_name = item.ref_no
    try:
        item.delete()
    except:
        messages.error(request, f'Product {item_name} cannot be deleted')
        return(redirect('inventory:update_product', pk=pk) )

    messages.success(request, f'Product {item_name} has been deleted')
    return redirect('inventory:products')

####Categories
@login_required    
@staff_user
def categories(request):
    """
    Vista para la gestión de categorías, incluida la creación, actualización y eliminación.
    """
    categories = Category.objects.all()
    dashboard_data = get_dashboard_data()

    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            cattype = "CAT"  
            cateNumber = create_ref_number(cattype, Category )
            form.ref_no = cateNumber 
            form.save()
            item_name = form.name
            messages.success(request,f'Category {item_name} has been created')
            return redirect('inventory:categories')

    else:
        form = CategoryForm()



    context = {
        'categories': categories,
        'form': form,
        **dashboard_data,

    }
    return render(request, 'inventory/dashboard/category_list.html', context)

@login_required    
@staff_user
def update_category(request, pk):
    """
    Vista para la actualización de una categoría existente.
    """
    category = Category.objects.get(id=pk)
    cateNumber = category.ref_no
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form = form.save(commit=False)
            form.ref_no = cateNumber
            form.save()
            item_name = category.name
            messages.success(request, f'Category {item_name} has been updated')
            return redirect('inventory:categories')
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category':category
    }
    return render(request, 'inventory/dashboard/category.html', context)


@login_required    
@staff_user
def delete_category(request, pk):
    """
    Elimina una categoría del inventario.
    """
    category= Category.objects.get(id=pk)
    item_name = category.ref_no
    try:
        category.delete()
    except:
        messages.error(request, f'Category {item_name} cannot be deleted')
        return(redirect('inventory:update_category', pk=pk) )
    
    messages.success(request, f'Category {item_name} has been deleted')
    return redirect('inventory:categories')    
   

##--------Orders------####
@login_required    
@staff_user
def orders(request):
    """
    Vista para mostrar la lista de pedidos en el panel de control.
    """
    order = Order.objects.all()
    dashboard_data = get_dashboard_data()

  
    context = {
        'order': order,
        **dashboard_data,
    }         
    return render(request, 'inventory/dashboard/order_list.html', context)




@login_required    
@staff_user
def create_or_update_order(request, pk=None):
    """
    Vista para la creación o actualización de un pedido en el inventario.
    """
    order_number = None
    no_editable = False
    if pk != None:
        order = get_object_or_404(Order, pk=pk)
        OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=0)
        
        if not request.user.is_superuser:
            if order.billing_status or order.saved_later:
                no_editable = True

    else:
        order = None
        ordtype = "ORD"
        order_number = create_ref_number(ordtype, Order, add_filter = True)
        OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

    

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)

        if form.is_valid() and formset.is_valid():
            """ That's useful when you get most of your model data from a form,
                but you need to populate some null=False fields with non-form data.
                Saving with commit=False gets you a model object, then you can add your extra data and save it.
            """
            form = form.save(commit=False)

            if pk == None:
                form.ref_no = order_number
                form.order_key = order_number

            if form.billing_status == True:
                form.billing_date = datetime.now()
     


            form.save()
            order_id = form.id
            formset.instance = form
            formset.save()
            
            if pk != None:
                order_instance = order
                order_instance.update_total_paid()
                item_name = form.ref_no
                messages.success(request, f'Order {item_name} has been updated')
                
            else:
                item_name = form.ref_no
                messages.success(request,f'Order {item_name} has been created')
            
            if form.billing_status:

                try:
                    
                    order_items = OrderItem.objects.filter(order=order_id) #Could be more than 1
                    for order_item in order_items:
                      
                        order_item.update_related_objects()
                        
                except:
                    error_message = "Check the stock of the product and update it"
                    messages.error(request, error_message)
                   
            

            return redirect('inventory:orders')  # Define a success URL or view
       
           
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)


    return render(request, 'inventory/dashboard/order.html', {'form': form, 'formset': formset, 'order': order ,  'order_number': order_number, 'no_editable':no_editable, })




@login_required    
@staff_user
def delete_order(request, pk):
    """
    Elimina un pedido del inventario.
    """
    item = Order.objects.get(id=pk)
    if item.saved_later:
        item_name = item.id
    else:
        item_name = item.ref_no

    item.delete()
    messages.success(request, f'Order {item_name} has been deleted')
    return redirect('inventory:orders')    



#####---------Customer---###
@login_required    
@staff_user       
def accounts(request):
    account = Customer.objects.all()
    dashboard_data = get_dashboard_data()
    context = {
        'accounts': account,
        **dashboard_data,

    }
    return render(request, 'inventory/dashboard/account_list.html', context)

##Update or create a customer (inventory)

@login_required    
@staff_user
def create_account(request):
    """
    Vista para la creación de una cuenta de usuario. 
    Se utiliza el formulario AccountFormCreate para recopilar la información del usuario,
    y luego se realiza el procesamiento necesario para crear la cuenta.
    """
    account = None
    if request.method == 'POST':
        form = AccountFormCreate(request.POST)
        if form.is_valid():
            """access cleaned_data and set the password on the form instance 
            (form.cleaned_data), not on the form class (AccountFormCreate.cleaned_data)."""
            # Create an instance of the model
            account = form.save(commit=False)

            # Set additional fields
            account.created_by = request.user

            # Set the password using set_password method
            account.set_password(form.cleaned_data['password'])

            # Save the instance
            account.save()
            
            item_name = account.email
            messages.success(request, f'Account {item_name} has been created')
            return redirect('inventory:accounts')  

    else:
        form = AccountFormCreate(instance=account)
    return render(request, 'inventory/dashboard/create_account.html', {'form': form, 'account': account })

@login_required    
@staff_user
def update_account(request, pk):
    """
    Vista para la actualización de una cuenta de usuario. 
    Se utiliza el formulario AccountFormUpdate para recopilar la información actualizada,
    y luego se realiza el procesamiento necesario para actualizar la cuenta.
    """
    account = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = AccountFormUpdate(request.POST, instance=account )
        if form.is_valid():
            form.save()

            item_name = account.email
            messages.success(request, f'Account {item_name} has been updated')

            return redirect('inventory:accounts')  
    else:
        form = AccountFormUpdate(instance=account )

    return render(request, 'inventory/dashboard/update_account.html', {'form': form, 'account': account })

@login_required    
@superuser_only
def delete_account(request, pk):
    """
    Elimina una cuenta del inventario.
    """
    account  = Customer.objects.get(id=pk)
    item_name = account.email
    account.delete()
    messages.success(request, f'Account {item_name} has been deleted')
    return redirect('inventory:accounts')


####-----Addresses----##
AddressFormSet = inlineformset_factory(Customer, Address, form=UserAddressForm, extra= 1, can_delete=True)
@login_required    
@staff_user
def create_or_update_addresses(request, pk):
    """
    Vista para la creación o actualización de direcciones asociadas a un usuario.
    Se utiliza un conjunto de formularios AddressFormSet para recopilar la información de las direcciones,
    y luego se realiza el procesamiento necesario para crear o actualizar las direcciones asociadas al usuario.
    """
    customer = Customer.objects.get(id=pk)
    addresses = Address.objects.filter(customer=pk)

    if request.method == 'POST':
        formset = AddressFormSet(request.POST, instance=customer, prefix='addresses')
        if formset.is_valid():
            formset.save()
            messages.success(request, f'Addresses for the user updated')
            return redirect('inventory:update_account',  pk=pk)  # Replace 'success_url' with the actual URL you want to redirect to

    else:
        formset = AddressFormSet(instance=customer, queryset=addresses, prefix='addresses')

    return render(request, 'inventory/dashboard/inventory_addresses.html', {'formset': formset, 'customer': customer})


#######------Suppliers-------####
@login_required    
@staff_user
def suppliers(request):
    """
    Vista para mostrar la lista de proveedores.
    Se obtienen todos los proveedores y se proporcionan datos al panel de control.
    """
    suppliers = Supplier.objects.all()
    dashboard_data = get_dashboard_data()


    context = {
        'suppliers': suppliers,
        **dashboard_data,
    }
    return render(request, 'inventory/suppliers/supplier_list.html', context)

##Create and Update a supplier (inventory)
@login_required    
@staff_user
def create_or_update_supplier(request, pk=None):
    """
    Vista para la creación o actualización de un proveedor.
    Se utiliza un formulario SupplierForm para recopilar la información del proveedor,
    y luego se realiza el procesamiento necesario para crear o actualizar el proveedor.
    """
    sup_number = None
    var_created_by = None
    if pk is not None:
        supplier = get_object_or_404(Supplier, pk=pk)
        var_created_by = supplier.created_by
      
    else:
        supplier = None
        suptype = "SUP"
        sup_number = create_ref_number(suptype, Supplier) 
       
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form = form.save(commit=False)
            
            if pk != None:
                item_name = supplier.ref_no
                form.created_by = var_created_by
                messages.success(request, f'Supplier {item_name} has been updated')
               
            else:
                form.ref_no = sup_number
                item_name =sup_number
                form.created_by = request.user

                messages.success(request,f'Supplier {item_name} has been created')
                

            form.save()
            return redirect('inventory:suppliers')  # Replace 'store:product_list' with the actual URL name for your product list view

    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'inventory/suppliers/supplier.html', {'form': form, 'supplier': supplier, 'sup_number': sup_number })       

@login_required    
@staff_user
def delete_supplier(request, pk):
    """
    Elimina un proveedor del inventario.
    """
    supplier = Supplier.objects.get(id=pk)
    item_name = supplier.ref_no
    try:
        supplier.delete()
    except:
        messages.error(request, f'Supplier {item_name} cannot be deleted')
        return(redirect('inventory:update_supplier', pk=pk) )
    
    messages.success(request, f'Supplier {item_name} has been deleted')
    return redirect('inventory:suppliers')

 
##-----invoices--##
@login_required    
@staff_user
def invoices(request):
    
    invoices = Purchase_invoice.objects.all()
    dashboard_data = get_dashboard_data()

    context = {  
        'invoices':invoices,
        **dashboard_data,

    } 
    return render(request, 'inventory/suppliers/invoice_list.html', context)
 

@login_required    
@staff_user
def create_or_update_invoice(request, pk=None):
    """
    Vista para la creación o actualización de una factura de compra.
    Se utiliza un formulario PurchaseInvoiceForm para recopilar la información de la factura,
    y un formulario PurchaseInvoiceDtlForms para recopilar la información detallada de la factura.
    Luego se realiza el procesamiento necesario para crear o actualizar la factura y sus detalles.

    """
    inv_number = None
    var_created_by = None
    invoice = None
    no_editable = False

    if pk != None:
        invoice = get_object_or_404(Purchase_invoice, pk=pk)
        var_created_by = invoice.created_by
        InvoiceDtlFormSet = inlineformset_factory(Purchase_invoice, Purchase_invoice_dtl, form=PurchaseInvoiceDtlForms, extra=0)

        if invoice.is_paid:
            if request.user.is_superuser:
                no_editable = False
            else:
                no_editable = True
        else:
            no_editable = False
    

    else: 
        pinvtype = "INV"  
        inv_number = create_ref_number(pinvtype, Purchase_invoice )
        InvoiceDtlFormSet = inlineformset_factory(Purchase_invoice, Purchase_invoice_dtl, form=PurchaseInvoiceDtlForms, extra=1)


    if request.method == 'POST':
 
        form = PurchaseInvoiceForm(request.POST, instance=invoice)
        formset = InvoiceDtlFormSet(request.POST, instance=invoice)

        
        if form.is_valid() and formset.is_valid():
          
            form = form.save(commit=False)
                
            if pk == None:
                form.ref_no = inv_number
                form.created_by = request.user
            else:
                form.created_by = var_created_by
                    
                
            form.save()
            formset.instance = form
            formset.save()

            if pk != None:

                invoice_instance = invoice
                invoice_instance.update_total_paid()

                invoice_items = Purchase_invoice_dtl.objects.filter(invoice=pk) #Could be more than 1
                for invoice_item in invoice_items:
                    invoice_item.update_related_objects()
                    

                item_name = invoice.ref_no
                messages.success(request, f'Invoice {item_name} has been updated')
                
            else:
                item_name = form.ref_no
                messages.success(request,f'Invoice {item_name} has been created')
           
            return redirect('inventory:invoices')  

            
    else:
        form = PurchaseInvoiceForm(instance=invoice)
        formset = InvoiceDtlFormSet(instance=invoice)
    
    return render(request, 'inventory/suppliers/invoice.html', {'form': form, 'formset': formset, 'inv_number': inv_number,'invoice': invoice, 'no_editable':no_editable})



@login_required    
@staff_user
def delete_invoice(request, pk):
    """
    Elimina una factura de compra del inventario.
    """
    invoice = Purchase_invoice.objects.get(id=pk)
    item_name = invoice.ref_no
    invoice.delete()
    messages.success(request, f'Invoice {item_name} has been deleted')
    return redirect('inventory:invoices')
 

##Una ventana emergente en la vista de inventario para mostrar los productos con un 90% de stock o menos.
def check_stock_notification(request):

    """
    Función para verificar las notificaciones de stock y desactivarlas si es necesario.
    Es parte de un sistema que maneja notificaciones de stock para productos.
    Recibe una solicitud HTTP desde la vista inventario.html y, a partir de los parámetros proporcionados, verifica y 
    desactiva las notificaciones de stock para los productos relevantes. 
    Retorna un objeto JSON que contiene mensajes informativos generados durante el proceso.
    """
    product_ids_string = request.GET.get('product_ids', '')  # Get the product_ids string from the query parameters
    product_ids = [int(id_product) for id_product in product_ids_string.split(',') if id_product.isdigit()]

    messages = []

    for product_id in product_ids:
        try:
            product = Product.objects.get(pk=product_id)
            if product.send_stock_notification:
                message = f'The stock for product "{product.name}" is at 90% or less of its maximum capacity.'
                product.send_stock_notification = False
                product.save()
                messages.append(message)
          
        except Product.DoesNotExist:
            message =f"Product with ID {product_id} does not exist."
            messages.append(message)

    return JsonResponse({'messages': messages})


def get_product_price(request, product_id):
    """
    Obtiene el precio de un producto para el formulario de órdenes
    """
    
    product = get_object_or_404(Product, pk=product_id)
    price = product.sell_price
    return JsonResponse({'price': str(price)})


def get_address_details(request, user_id):
    """
    Obtiene los detalles de la dirección predeterminada de un usuario para su uso 
    en el formulario de órdenes
    """
    try:
        address = get_object_or_404(Address, customer=user_id, default = True)
       
        address_details = {
            'full_name': address.full_name,
            'email': address.email,
            'address1': address.address_line,
            'address2': address.address_line2,
            'country': address.country,
            'city': address.town,
            'contact_no': address.phone,
            'post_code': address.postcode,
        }
        return JsonResponse(address_details)
 
    except Address.DoesNotExist:
        return JsonResponse({'error': 'Address not found for the given customer ID'}, status=404)



def get_supplier_products(request, supplier_id):
    """Obtiene los productos de un proveedor para su en el formulario de factura."""
    products = Product.objects.filter(supplier_id=supplier_id, is_active = True).values('id', 'name')
    return JsonResponse(list(products), safe=False)

