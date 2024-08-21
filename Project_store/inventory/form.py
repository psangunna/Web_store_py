from django import forms
from store.models import Product, Category
from account.models import Customer
from orders.models import Order, OrderItem
from django.forms import inlineformset_factory 
from django.utils.translation import gettext_lazy as _
from suppliers.models import Supplier

# Formulario para la creación de cuentas de usuario
class AccountFormCreate(forms.ModelForm):
    # Campos adicionales para username, email, password, y número de contacto
    # Incluye validaciones personalizadas para username, password y email
    user_name = forms.CharField(
        label='Enter Username', min_length=4, max_length=50)
    email = forms.EmailField(max_length=100, error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'minlength': '6', 'maxlength': '20'}))
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(attrs={'minlength': '6', 'maxlength': '20'}),  # Adjust the length as needed
    )
    mobile = forms.CharField(
        label='Contact nº', min_length=8, max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Contact nº', 'id': 'form-mobile'}))
    
    class Meta:
        model = Customer
        fields = '__all__'

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = Customer.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email
    
    def __init__(self, *args, **kwargs):
        # Configuración adicional de widgets y atributos para la presentación del formulario
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})
        self.fields['mobile'].required = False

        
# Formulario para la actualización de cuentas de usuario
class AccountFormUpdate(forms.ModelForm):
    # Campo adicional para número de contacto
    mobile = forms.CharField(
        label='Contact nº', min_length=8, max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Contact nº', 'id': 'form-mobile'}))
    
    class Meta:
        model= Customer
        fields = ('email', 'user_name', 'mobile', 'is_active', 'is_staff', 'is_superuser','last_login')
    
    def __init__(self, *args, **kwargs):
        # Configuración adicional de widgets y atributos para la presentación del formulario
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['last_login'].widget.attrs['readonly'] = True
        self.fields['mobile'].required = False


# Formulario para la creación/actualización de categorías
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ref_no'].widget = forms.HiddenInput()

# Formulario para la creación/actualización de productos
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product 
        fields = '__all__'
       
        
        widgets = { 
            
            'description': forms.Textarea(attrs={
                'class': 'py-1 px-6 rounded-xl border'
            }),
        }
        

    def __init__(self, *args, **kwargs):
        # Configuración adicional para la presentación del formulario
        super().__init__(*args, **kwargs)
        self.fields['ref_no'].widget.attrs['readonly'] = True
        # Filtra las opciones de proveedores para incluir solo proveedores activos
        self.fields['supplier_id'].queryset = Supplier.supplier.all()
  
# Formulario para la creación/actualización de pedidos
class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'


