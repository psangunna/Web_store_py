from .basket import Basket

"""Este código actúa como un "context processor" en Django. 
Un context processor es una función que añade variables específicas al contexto de cada template renderizado. 
En este caso, el context processor asegura que el objeto Basket esté disponible en el contexto de todos los templates.
Para utilizar este context processor, se ha agregado a la configuración de context processors de Django, en el archivo settings.py bajo la configuración TEMPLATES """
def basket(request):
    return {'basket': Basket(request)}