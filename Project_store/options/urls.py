from django.urls import include, path

from . import views

app_name = "options"

urlpatterns = [
    path("delivery_address/", views.delivery_address, name="delivery_address"),
]