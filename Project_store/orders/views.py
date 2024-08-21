from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from basket.basket import Basket
from .models import Order, OrderItem
from account.models import  Address
from datetime import datetime
import plotly.express as px
import plotly
import json
import pandas as pd
from django_pandas.io import read_frame
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages

def add(request):
    """
    Añade productos al carrito y crea una orden cuando se realiza el pago.
    """
    basket = Basket(request)
  
    if request.POST.get('action') == 'post':
       
        order_key = request.POST.get('order_key')
        user_id = request.user.id

        address=get_object_or_404(Address, customer=user_id, default=True)
      

        baskettotal = basket.get_total_price()

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
           
            
            order = Order.objects.create(user_id=user_id, full_name=address.full_name, contact_no = address.phone,email=address.email, address1=address.address_line,
                                        address2=address.address_line2, country=address.country, city=address.town, post_code=address.postcode, total_paid=baskettotal, shipping = 11.50 , order_key=order_key)
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])
             
        response = JsonResponse({'success': 'Return something'})
        return response


def payment_confirmation(data):
    """
    Confirma el pago de una orden y actualiza el estado de facturación y la fecha de facturación.
    """
    Order.objects.filter(order_key=data).update(billing_status=True, billing_date = datetime.now())
    order_created = get_object_or_404(Order,order_key=data)
    order_item = OrderItem.objects.get(order=order_created.id)  # actual ID
    order_item.update_related_objects() #Update the quantity in products


def user_orders(request):
    """
    Retorna todas las órdenes facturadas de un usuario.
    """
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders


@login_required
def savedOrder_later(request):
    """
    Crea una orden y la marca como guardada para más tarde.
    """
    basket = Basket(request)
    baskettotal = basket.get_total_price()
    user = request.user

    order = Order.objects.create(user_id=user.id,saved_later = True, total_paid=baskettotal, shipping = 11.50)
    
    order_id = order.pk

    for item in basket:
        OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])

    basket.clear()
    return render(request, 'payment/order_saved.html')



def savedOrder_add(request, pk):
    """
    Añade una orden guardada previamente por el usaurio al carrito.
    """
    basket = Basket(request)
    order  = get_object_or_404(Order, id= pk)
    detalles = OrderItem.objects.filter(order = order.id)
    

    for order_detalle in detalles:
        product_qty =  order_detalle.quantity
        basket.add(product=order_detalle.product, qty=product_qty)

    order.delete() 
    messages.success(request, f'Order has been add back to the basket')

    return redirect('account:user_orders')


def savedOrder_delete(request, pk):
    """
    Elimina una orden guardada previamente por el usuario.
    """
    order  = get_object_or_404(Order, id= pk)
    order.delete() 
    messages.success(request, f'Order has been deleted')

    return redirect('account:user_orders')


def shopping_chart(request):
    """
    Genera un gráfico de barras que muestra las compras realizadas por un usuario.
    """

    id_user = request.user
    orders = Order.objects.all().filter(billing_status=True, user = id_user)
    if orders.exists():
        # Create a DataFrame from the QuerySet
        df =  read_frame(orders)

        df['billing_date'] = pd.to_datetime(df['billing_date']).dt.strftime('%Y-%m-%d')
  
    #Bar graph
    # Group by billing_date and sum total_paid for each date
        shopping_chart_df = df.groupby(by="billing_date")['total_paid'].sum().reset_index()

    # Create a bar chart
        shopping_chart = px.bar(shopping_chart_df,
                                x=shopping_chart_df['billing_date'],
                                y=shopping_chart_df['total_paid'],
                                orientation='v',  # Set orientation to horizontal
                                #title="Purchase Trend"
                                )

        # Customize the layout
        shopping_chart.update_layout(
            xaxis_title="Purchase Date",
            yaxis_title="Purchase Total (€)",
            plot_bgcolor='white',  # Set background color
            paper_bgcolor='white',  # Set paper color
            font=dict(color='black'),  # Set font color
            bargap=0.2,  # Set gap between bars
            xaxis=dict(
               
                tickformat="%b %d %Y",
               
            )

        )

        # Customize the color of bars
        shopping_chart.update_traces(marker_color= 'rgb(255, 193, 7)')  # Set color to blue

        shopping_chart = json.dumps(shopping_chart, cls=plotly.utils.PlotlyJSONEncoder)

   
    else:
        shopping_chart = None

    context = {'shopping_chart': shopping_chart }


    
    return render(request, 'account/dashboard/shopping_chart.html', context )
