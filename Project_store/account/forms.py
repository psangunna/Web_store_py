from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)

from .models import Customer,Address

# Formulario para la dirección del usuario
class UserAddressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = ["full_name", "phone","email",  "address_line", "address_line2", "town", "country","postcode", "default"]

# Formulario de inicio de sesión del usuario
class UserLoginForm(AuthenticationForm):
    # Campos personalizados para el formulario de inicio de sesió
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))

# Formulario de registro de usuario
class RegistrationForm(forms.ModelForm):
    # Campos personalizados para el formulario de registro

    user_name = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'minlength': '6', 'maxlength': '20'}),  # Adjust the length as needed
    )
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(attrs={'minlength': '6', 'maxlength': '20'}),  # Adjust the length as needed
    )

    class Meta:
        model = Customer
        fields = ('user_name', 'email',)

    # Validaciones personalizadas para el formulario de registro
    def clean_username(self):
        # Verifica si el nombre de usuario ya existe
        user_name = self.cleaned_data['user_name'].lower()
        r = Customer.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name
    
    def clean_password2(self):
        # Verifica si las contraseñas coinciden
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        # Verifica si la dirección de correo electrónico ya está en uso
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another email, that is already taken')
        return email
    
    def __init__(self, *args, **kwargs):
        # Personaliza la apariencia de los campos del formulario
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})

# Formulario para restablecer la contraseña 
class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))


    def clean_email(self):
        # Verifica si la dirección de correo electrónico es válida
        email = self.cleaned_data['email']
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email

# Formulario para confirmar el restablecimiento de la contraseña
class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))
 

# Formulario para editar la información del usuario
class UserEditForm(forms.ModelForm):
    # Campos para editar la información del usuario

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Name', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Name', 'id': 'form-user_name',}))

    mobile = forms.CharField(
        label='Mobile', min_length=8, max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Mobile', 'id': 'form-mobile'}))
    
    class Meta:
        model =Customer
        fields = ('email', 'user_name', 'mobile',)
    

    def __init__(self, *args, **kwargs):
        # Define la obligatoriedad de algunos campos y personaliza la apariencia
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True
        self.fields['mobile'].required = False