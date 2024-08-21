from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventory.decorators import staff_user
from store.models import Product
from orders.models import Order, OrderItem
from django.db.models import Count, Sum
from suppliers.models import  Purchase_invoice_dtl
from inventory.inventory_management import InventoryManager
import plotly.express as px
import plotly
import json
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from django.db.models import Count, Sum
from django.db.models.functions import TruncWeek

@login_required    
@staff_user
def dashboard_graphs(request):
    """Renderiza la plantilla 'dashboard.html' para el panel de control."""
    return render(request, 'inventory/graphs/dashboard.html')


@login_required    
@staff_user
def sales_trend(request):
    """Muestra una gráfica de tendencia de ventas a lo largo del tiempo utilizando datos del inventario."""
    products = Product.products.all()
  
    inventory_data = InventoryManager.get_inventory_data(products)
    sales_graph_json = None
       #chart1 
    if len(inventory_data) > 0:
        df = pd.DataFrame(inventory_data)
        """Los datos se agrupan por la columna 'last_sales_date', sumando las ventas para cada fecha.
        El resultado se convierte a formato JSON para ser utilizado en la visualización de la gráfica."""
        # Convertir 'last_sales_date' a fecha y hora y extraer solo la parte de la fecha
        df['last_sales_date'] = pd.to_datetime(df['last_sales_date']).dt.strftime('%Y-%m-%d')
        df['updated_stock_at'] = pd.to_datetime(df['updated_stock_at']).dt.strftime('%Y-%m-%d')
        sales_graph = df.groupby(by="last_sales_date",as_index=False, sort=True,)['sales'].sum()
      
        # Convert the result to JSON
        """se pasa el JSON creado para ser utilizado en la plantilla, desde donde
        se customiza a gráfica"""
        sales_graph_json = sales_graph.to_json(orient='records', date_format='iso')
    


    return render(request, 'inventory/graphs/sales_trend.html', {'sales_graph':sales_graph_json})

@login_required    
@staff_user
def product_perform(request):
    """Muestra una gráfica de barras horizontal que representa el rendimiento de los productos en términos de cantidad vendida."""
    products = Product.products.all()
    inventory_data = InventoryManager.get_inventory_data(products)
    best_performing_product = None
    if len(inventory_data) > 0:
        df = pd.DataFrame(inventory_data)
        df['last_sales_date'] = pd.to_datetime(df['last_sales_date']).dt.strftime('%Y-%m-%d')
        df['updated_stock_at'] = pd.to_datetime(df['updated_stock_at']).dt.strftime('%Y-%m-%d')
        #chart2
        best_performing_product_df = df.groupby(by="product").sum().sort_values(by = "sold")
        best_performing_product = px.bar(best_performing_product_df,
                                            x = best_performing_product_df.index,
                                            y = best_performing_product_df.sold,
                                            )
    # Customizar the layout
        best_performing_product.update_layout(
            xaxis_title="Products",
            yaxis_title="Quantity Sold",
            plot_bgcolor='white',  # background color
            paper_bgcolor='white',  # paper color
            font=dict(color='black'),  # font color
            bargap=0.2,  # Set gap between bars
        )

        # Customizar the color de las barras
        best_performing_product.update_traces(marker_color='rgba(255, 99, 132, 1)')  # Set color to blue


        best_performing_product = json.dumps(best_performing_product,cls=plotly.utils.PlotlyJSONEncoder )
        
    return render(request, 'inventory/graphs/product_perform.html', {'best_performing_product': best_performing_product})


@login_required    
@staff_user
def product_stock(request):
    """Muestra un pie chart que visualiza la cantidad de stock para los diferentes productos."""
    products = Product.products.all()
    inventory_stock =[]

    for product in products:
        stock = product.stock_real
        
        inventory_stock.append({
            'product': product.name,
            'stock': stock,
        })

    most_product_in_stock = None
    if len(inventory_stock) > 0:
        df = pd.DataFrame(inventory_stock)

        most_product_in_stock_df = df.groupby(by="product").sum().sort_values(by = "stock")
        most_product_in_stock = px.pie(most_product_in_stock_df,
                                            names = most_product_in_stock_df.index,
                                            values = most_product_in_stock_df.stock,
                            
                                            )
        # Customizar the layout
        most_product_in_stock .update_layout(
            plot_bgcolor='white',  #  background color
            paper_bgcolor='white',  #  paper color
            font=dict(color='black'),  #  font color
        )   

        most_product_in_stock = json.dumps(most_product_in_stock,cls=plotly.utils.PlotlyJSONEncoder )
        
    return render(request, 'inventory/graphs/product_stock.html', {'most_product_in_stock': most_product_in_stock})



def get_product_info_per_week():
    """Obtiene información sobre los productos vendidos por semana."""

    
    """Se realiza una consulta a la base de datos de Facturas y se filtra las facturas pagadas (invoice__is_paid=True),
    agrega el campo semana de la factura y realiza agregaciones para obtener la cantidad total y el precio total por producto por semana. 
    Luego, los resultados se ordenan por semana y nombre del producto."""
    product_info_per_week = Purchase_invoice_dtl.objects.filter(invoice__is_paid=True) \
        .annotate(week=TruncWeek('invoice__paid_at')) \
        .values('week', 'product__name') \
        .annotate(total_quantity=Sum('qty'), total_price=Sum('amount')) \
        .order_by('week', 'product__name')

    result = {}
    """Se itera sobre los resultados de la consulta y
    se organiza la información en un diccionario --> result"""
    for product_data in product_info_per_week:
        week = product_data['week']
        product_name = product_data['product__name']
        total_quantity = product_data['total_quantity']
        total_price = product_data['total_price']

        if week not in result:
            result[week] = []

        result[week].append({
            'product_name': product_name,
            'total_quantity': total_quantity,
            'total_price': total_price,
        })

    return result

def get_order_info_per_week():
    """Obtiene información sobre las órdenes realizadas por semana, 
    incluyendo detalles de productos."""


    order_info_per_week = Order.objects.filter(billing_status=True) \
        .annotate(week=TruncWeek('billing_date')) \
        .values('week') \
        .annotate(total_orders=Count('id')) \
        .order_by('week')

    product_info_per_week = OrderItem.objects.filter(order__billing_status=True) \
        .annotate(week=TruncWeek('order__billing_date')) \
        .values('week', 'product__name') \
        .annotate(total_quantity=Sum('quantity'), total_price=Sum('amount')) \
        .order_by('week', 'product__name')

   
    # Organiza los datos en diccionarios.
    order_result = {}
    for order_data in order_info_per_week:
        week = order_data['week']
        total_orders = order_data['total_orders']

        if week not in order_result:
            order_result[week] = {'total_orders': total_orders, 'products': []}

    for product_data in product_info_per_week:
        week = product_data['week']
        product_name = product_data['product__name']
        total_quantity = product_data['total_quantity']
        total_price = product_data['total_price']

        order_result[week]['products'].append({
            'product_name': product_name,
            'total_quantity': total_quantity,
            'total_price': total_price,
        })

    return order_result


@login_required    
@staff_user
def product_info_per_week_view(request):
    """Presenta gráficamente la información sobre productos y órdenes por semana,
    mostrando los precios totales en un gráfico de barras."""

    #Se obtienen datos relacionados con productos y órdenes
    product_info_per_week = get_product_info_per_week()
    order_info_per_week = get_order_info_per_week()

    # Extraer fechas y precios totales de todos los productos y pedidos.
    all_product_dates = []
    all_product_prices = []
    all_order_dates = []
    all_order_prices = []
    #Se itera sobre los datos de productos y órdenes por semana para extraer las fechas y calcular los precios totales.
    for week, products in product_info_per_week.items():
        all_product_dates.append(week.strftime('%Y-%m-%d'))
        all_product_prices.append(sum(product['total_price'] for product in products))

    for week, order_data in order_info_per_week.items():
        all_order_dates.append(week.strftime('%Y-%m-%d'))
        all_order_prices.append(sum(product['total_price'] for product in order_data['products']))

   
    """Se crean dos objetos Bar (traces) utilizando la biblioteca Plotly. 
    Cada trace representa productos u órdenes, respectivamente, en el gráfico de barras."""
   
    trace_product = go.Bar(
        x=all_product_dates,
        y=all_product_prices,
        name='Products',
        marker=dict(color='rgba(255, 99, 132, 1)')
    )

    trace_order = go.Bar(
        x=all_order_dates,
        y=all_order_prices,
        name='Orders',
         marker=dict(color= 'rgba(17, 6, 237, 0.746)')
    )

    layout = go.Layout(barmode='group',xaxis=dict(title='Week'), yaxis=dict(title='Cost(€)'), plot_bgcolor="white", paper_bgcolor= 'rgb(255,255,255)')
    fig = make_subplots(rows=1, cols=1)
    fig.update_layout(layout)

    fig.add_trace(trace_product)
    fig.add_trace(trace_order)

    graph_div2 = fig.to_html(full_html=False)

    context = {
        'graph_div2': graph_div2,
        'product_info_per_week': product_info_per_week,
        'order_info_per_week': order_info_per_week,
    }
    
    return render(request, 'inventory/graphs/product_order.html', context)
