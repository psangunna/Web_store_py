from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from orders.models import Order
from orders.views import user_orders
from store.views import Product, Category
from .forms import RegistrationForm, UserEditForm, UserAddressForm
from .models import Customer, Address
from .tokens import account_activation_token

# Vista para mostrar productos en la página principal
def items(request):
    # Obtiene productos activos y categorías

    items = Product.objects.filter(is_active = True)[0:6]
    categories = Category.objects.all()
    return render(request,'index_puddle.html', {'categories': categories,
                                               'items': items, })
    
# Vista del panel de control del usuario
@login_required
def dashboard(request):
    # Obtiene y muestra los pedidos del usuario
    orders = user_orders(request)
    return render(request,
                  'account/dashboard/dashboard.html',
                  {'section': 'profile', 'orders': orders})

   
# Vista para editar detalles del usuario
@login_required 
def edit_details(request):
    # Edita los detalles del usuario si se envía un formulario válido
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:   
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/dashboard/edit_details.html', {'user_form': user_form})

  
# Vista para desactivar la cuenta del usuario
@login_required
def delete_user(request):
    # Desactiva la cuenta del usuario, lo desconecta y redirige a la confirmación de eliminación
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


# Vista para el registro de cuenta de usuario
def account_register(request):
    # Registra una nueva cuenta de usuario, envía correo de activación y muestra confirmación

    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password']) #hash the password before saving it to the database
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'account/registration/register_email_confirm.html', {'form': registerForm})
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


# Vista para activar la cuenta de usuario
def account_activate(request, uidb64, token):
    # Activa la cuenta del usuario y redirige al panel de control
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')

 

 
# Vista para ver las direcciones del usuario
@login_required
def view_address(request):
    # Obtiene y muestra las direcciones del usuario
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})
   

# Vista para agregar una nueva dirección del usuario
@login_required
def add_address(request):
    # Agrega una nueva dirección si se envía un formulario válid
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})
 
# Vista para editar una dirección existente del usuario
@login_required
def edit_address(request, id):
    # Edita una dirección existente si se envía un formulario válido
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save() 
            return HttpResponseRedirect(reverse("account:addresses"))

    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})

# Vista para eliminar una dirección del usuario
@login_required
def delete_address(request, id):
    # Elimina una dirección existente del usuario
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("account:addresses")



# Vista para establecer una dirección como predeterminada
@login_required
def set_default(request, id):
    # Establece una dirección como predeterminada y redirige según la URL anterior
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)

    previous_url = request.META.get("HTTP_REFERER")

    if "delivery_address" in previous_url:
        return redirect("options:delivery_address")

    return redirect("account:addresses")


# Vista para mostrar los pedidos del usuario
@login_required
def user_orders(request):
    # Obtiene y muestra los pedidos del usuario
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id)        
    return render(request, "account/dashboard/user_orders.html", {"orders": orders})




