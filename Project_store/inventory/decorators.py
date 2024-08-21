from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
"""
Se define dos decoradores personalizados (staff_user y superuser_only) 
 que se utilizan para restringir el acceso a ciertas vistas basándose en 
 el tipo de usuario que ha iniciado sesión.
"""

"""Este decorador verifica si el usuario actual es un superusuario o un usuario con privilegios de staff.
Si el usuario tiene estos privilegios, la vista original (view_func) se llama y se procesa normalmente.
Si el usuario no tiene estos privilegios, se redirige a la página con nombre 'store_management'."""
def staff_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_superuser or request.user.is_staff :
			return view_func(request, *args, **kwargs)
		else:
			return redirect('store_management')
			

	return wrapper_func


"""Este decorador verifica si el usuario actual es un superusuario.
Si el usuario es un superusuario, la vista original se llama y se procesa normalmente.
Si el usuario no es un superusuario, se muestra un mensaje de error
y se renderiza un template de error ('inventory/auth_error.html')."""
def superuser_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request,'You are not authorized to perform the action' )
            return render(request, 'inventory/auth_error.html')
    return wrapper_function