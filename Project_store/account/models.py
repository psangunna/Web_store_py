import uuid
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
    
# Manager personalizado para el modelo Customer
class CustomAccountManager(BaseUserManager):
    # Método para crear un superusuario
    def create_superuser(self, email, user_name, password, **other_fields):
        # Asegura que las configuraciones para superusuario estén activadas
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        # Verifica que el superusuario sea un miembro del personal
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        # Verifica que el superusuario tenga permisos de superusuario
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
         # Crea y guarda el superusuario
        return self.create_user(email, user_name, password, **other_fields)

     # Método para crear un usuario regular
    def create_user(self, email, user_name, password, **other_fields):
         # Verifica que se proporcione una dirección de correo electrónico

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user
 
#Modelo de usuario personalizado que hereda de AbstractBaseUser y PermissionsMixin
class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    user_name = models.CharField(max_length=150)
    mobile = models.CharField(_('Contact nº'),max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, help_text= '(Employees)')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 
    # Asigna el objeto del manager personalizado
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"
    # Método para enviar un correo electrónico al usuario
    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.user_name

# Modelo para almacenar direcciones asociadas a los usuarios
class Address(models.Model):
   
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.CASCADE)
    full_name = models.CharField(_("Full Name"), max_length=150)
    phone = models.CharField(_("Contact Number"), max_length=50)
    postcode = models.CharField(_("Postcode"), max_length=50)
    email = models.EmailField(_("Email"), blank = True)
    address_line = models.CharField(_("Address Line 1"), max_length=255,)
    address_line2 = models.CharField(_("Address Line 2"), max_length=255, blank = True)
    town = models.CharField(_("Town/City/State"), max_length=150)
    country = models.CharField(_("Country"), max_length=150)
    delivery_instructions = models.CharField(_("Delivery Instructions"), max_length=255)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)
 
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return "Address"
    