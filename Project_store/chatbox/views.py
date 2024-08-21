from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from orders.models import Order
from account.models import Customer
from .forms import ConversationMessageForm
from .models import Conversation

@login_required
def new_conversation(request, order_pk):
    """
    Se crea una nueva conversación relacionada con un pedido y envía un mensaje inicial.
    Si ya existe una conversación relacionada con el pedido, se redirige a esa conversación.
    """
    order = get_object_or_404(Order, pk=order_pk)

    conversations = Conversation.objects.filter(order=order).filter(members__in=[request.user.id])

    if conversations:
        return redirect('chatbox:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(order=order)
            conversation.members.add(request.user) 
            list_admin = Customer.objects.filter(is_superuser=True)
            # Suponiendo que list_admin es una lista de objetos administradores de Clientes
            for admin in list_admin:
                conversation.members.add(admin)

            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            messages.success(request,'Message sent')
            return redirect('account:user_orders')
    else:
        form = ConversationMessageForm()
    
    return render(request, 'chatbox/chatbox.html', {
        'form': form
    })

@login_required
def inbox(request):
    """
    Muestra la bandeja de entrada del usuario con las conversaciones creadas.
    """
    user_id = request.user.id
    conversations = Conversation.objects.filter(members__in=[request.user.id])
   
    for conversation in conversations:
        print (conversation.order)
        
        

    return render(request, 'chatbox/inbox.html', {
        'conversations': conversations
    })

@login_required
def detail(request, pk):
    """
    Muestra los detalles de una conversación y permite al usuario enviar mensajes.
    """
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
    
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('chatbox:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'chatbox/detail.html', {
        'conversation': conversation,
        'form': form
    })

@login_required
def admin_inbox(request):
    """
    Muestra la bandeja de entrada de los administradores con las conversaciones disponibles.
    """
    user_id = request.user.id
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)

    for conversation in conversations:
        print (conversation.order)
        
        

    return render(request, 'inventory/chatbox/admin_inbox.html', {
        'conversations': conversations
    })


@login_required
def detail_inbox(request, pk):
    """
    Muestra los detalles de una conversación en la bandeja de entrada de los administradores.
    """
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
   
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('chatbox:detail_inbox', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'inventory/chatbox/detail_inbox.html', {
        'conversation': conversation,
        'form': form
    })

@login_required
def delete_message(request, pk):
    """
    Elimina una conversación y redirige a la bandeja de entrada de los administradores.
    """
    conversacion = Conversation.objects.get(id=pk)
    conversacion.delete()
    messages.success(request, f'The messsage has been deleted')
    return redirect('chatbox:admin_inbox')

        

