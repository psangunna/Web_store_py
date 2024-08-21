from django.contrib.auth.models import User
from django.db import models
from orders.models import Order
from django.conf import settings

# Modelos de Conversación para el sistema de mensajería
# Una conversación está asociada a un pedido y tiene varios miembros (usuarios)
class Conversation(models.Model):
    order = models.ForeignKey(Order, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-modified_at',)

# Modelo para los mensajes dentro de una conversación
class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_messages', on_delete=models.CASCADE)