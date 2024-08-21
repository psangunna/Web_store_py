from orders.models import  Order

#Clase para gestionar la generación de datos de inventario
#Este método toma una lista de productos y genera datos de inventario para cada producto. 
#Itera sobre los productos, examina los elementos de pedido asociados y calcula varias métricas relacionadas con el inventario, como la cantidad vendida, los ingresos, la última fecha de venta, etc. 
#Finalmente devuelve una lista de diccionarios que contiene estos datos para cada producto.
class InventoryManager:
    @staticmethod
    def get_inventory_data(products):
        # Lista para almacenar los datos de inventario para cada producto
        inventory_data = []
        cost = None

        # Selecciona todos los pedidos pagados
        OrderAll = Order.objects.filter(billing_status=True)
    
        # Itera sobre cada producto
        for product in products:
            stock = product.stock_real
            # Obtiene todos los elementos de pedido para este producto, ordenados por orden
            order_items = product.order_items.order_by('order').all()

            firstFound = False
            last_order = None
            total_quantity = 0

            # Itera sobre los elementos de pedido para calcular el total vendido
            for order_item in order_items:
                id_order = str(order_item.order)
                order_paid = OrderAll.filter(id=id_order)
               
                if order_paid.exists():
                    total_quantity += order_item.quantity
                    
                    if not firstFound:
                        last_order = order_item
                        firstFound = True                   

            # Obtiene la fecha de la última venta para el producto
            if last_order is not None:
                id_order = last_order.order
                id_order = str(id_order)
                last_order_paid = Order.objects.get(id=id_order)
                last_sale = last_order_paid.billing_date
                last_sale_date = last_sale
                
            else:
                last_sale_date = None
            
            # Calcula las métricas de inventario
            stock_sold = total_quantity
            revenue = stock_sold * product.sell_price

            if product.stock_real is not None:
                cost = product.stock_real * product.buy_price
            
            # Agrega los datos de inventario a la lista
            inventory_data.append({
                'product': product.name,
                'stock': stock,
                'sold': stock_sold,
                'cost_per_item': product.sell_price,
                'buy_cost': product.buy_price,
                'sales': revenue,
                'last_sales_date': last_sale_date,
                'cost': cost,
                'stock_max': product.stock_max,
                'check_stock': product.send_stock_notification,
                'updated_stock_at': product.updated_stock_at
            })
        
        # Devuelve la lista de datos de inventario
        return inventory_data