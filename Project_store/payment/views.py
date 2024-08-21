import json
import os
from django.contrib import messages  
import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.conf import settings
from basket.basket import Basket
from orders.views import payment_confirmation
from orders.forms import OrderForm
from account.models import Address
from django.shortcuts import get_object_or_404

def order_placed(request):
    """
    Vista para la página de confirmación de pedido.
    Limpia la cesta después de que se realice un pedido.
    """
    basket = Basket(request)
 
    basket.clear()
    return render(request, 'payment/orderplaced.html')


class Error(TemplateView):
    """
    Vista para mostrar un mensaje de error personalizado.
    Utilizada para mostrar errores relacionados con el pago.
    """
    template_name = 'payment/error.html'


@login_required
def BasketView(request):
    """
    Vista para la pantalla de pago que utiliza Stripe.
    Crea un intento de pago y renderiza el formulario de pago.
    """
    user_id = request.user
    try:
        address=get_object_or_404(Address, customer=user_id, default=True)
    except:
        messages.warning(request, f'Select an address')
        return redirect('options:delivery_address')

    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    form = OrderForm()

    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/payment_form.html', {'client_secret': intent.client_secret,'STRIPE_PUBLISHABLE_KEY': os.environ.get('STRIPE_PUBLISHABLE_KEY'), 'form': form})
  
@csrf_exempt
def stripe_webhook(request):
    """
    Vista para manejar eventos de webhook de Stripe, como pagos exitosos.
    """
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return HttpResponse(status=400)

    # Manejar el evento
    if event.type == 'payment_intent.succeeded':
        
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)


