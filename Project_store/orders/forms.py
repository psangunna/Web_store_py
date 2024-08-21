from django import forms
from .models import Order, OrderItem
from store.models import Product
from django.utils.translation import gettext_lazy as _

class OrderForm(forms.ModelForm):
    """
    Formulario para el modelo Order.
    """
    class Meta: 
        model = Order
        fields = ['ref_no','user', 'full_name', 'email', 'address1', 'address2', 'city','country' ,'contact_no', 'post_code', 'total_paid','shipping' ,'order_key', 'billing_status']
        
        widgets = {
            'user': forms.Select(attrs={
                'class': 'wd-50 '

            }),
            'full_name': forms.TextInput(attrs={
                'class': 'wd-100 '}),
            
            'adress1': forms.TextInput(attrs={
                'class': 'wd-100 '
            
            }),              
            'total_paid': forms.TextInput(attrs={
                'class': 'w-50'
            }),
            'shipping': forms.TextInput(attrs={
                'class': 'w-50'
            }),            
            'billing_status': forms.CheckboxInput(attrs={'class': 'width-20px  height-10px margin-right-5px'})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_key'].widget.attrs['readonly'] = True
        self.fields['ref_no'].widget.attrs['readonly'] = True
        self.fields['total_paid'].label= _('Total €')
        self.fields['shipping'].label= _('Shipping €')
        self.fields['shipping'].widget.attrs['readonly'] = True
        self.fields['total_paid'].widget.attrs['readonly'] = True
       
        
        
class OrderItemForm(forms.ModelForm):
    """
    Formulario para el modelo OrderItem.
    """
    class Meta:
        model = OrderItem
        fields = ['product', 'price', 'quantity', 'amount']
        widgets ={ 
            'product': forms.Select(attrs={'class': 'w-100 h-100 px-2 select_product', 
            }),

            'price': forms.TextInput(attrs={
                'class': 'w-100 update_price'
            }),
            'quantity': forms.TextInput(attrs={
                'class': 'w-100 '
            }),
            'amount': forms.TextInput(attrs={
                'class': 'w-100'
            }),             
            
            }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['readonly'] = True
        self.fields['price'].widget.attrs['readonly'] = True
        self.fields['product'].queryset = Product.objects.filter(is_active=True)