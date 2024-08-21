from django.urls import path
from . import views

app_name='chatbox'

urlpatterns = [
    path('new/<int:order_pk>/', views.new_conversation, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('inbox/', views.inbox, name='inbox'),
    path('admin_inbox/', views.admin_inbox, name='admin_inbox'),
    path('detail_inbox/<int:pk>/', views.detail_inbox, name='detail_inbox'),
    path('delete_message/<int:pk>', views.delete_message, name='delete_message')
    ]