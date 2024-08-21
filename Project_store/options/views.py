from account.models import Address
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def delivery_address(request):
    """
    Vista que maneja las direcciones de entrega del usuario autenticado.

    Requiere que el usuario esté autenticado antes de acceder a esta vista.

    Parameters:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: Renderiza la página 'options/delivery_address.html' con las direcciones del usuario.
    """
    # Obtiene la sesión actual del usuario
    session = request.session

    # Filtra las direcciones del usuario autenticado, ordenadas por la predeterminada primero
    addresses = Address.objects.filter(customer=request.user).order_by("-default")

    # Si existen direcciones, realiza las siguientes acciones
    if addresses.exists():
        # Si no hay una dirección almacenada en la sesión, utiliza la primera dirección como predeterminada
        if "address" not in request.session:
            session["address"] = {"address_id": str(addresses[0].id)}
        else:
            # Actualiza la dirección almacenada en la sesión si ya existe
            session["address"]["address_id"] = str(addresses[0].id)
            session.modified = True

    # Renderiza la página 'options/delivery_address.html' con las direcciones del usuario
    return render(request, "options/delivery_address.html", {"addresses": addresses})

