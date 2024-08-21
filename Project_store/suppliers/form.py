from django import forms
from suppliers.models import Supplier, Purchase_invoice_dtl, Purchase_invoice
from django.utils.translation import gettext_lazy as _

# Formulario para el modelo Supplier
class SupplierForm(forms.ModelForm):
    class Meta:
        model= Supplier
        fields = '__all__'
        # Configuración de widgets para campos específicos
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'py-1 px-2 rounded-xl border'
            }),
            'ref_no': forms.TextInput(attrs={
                'class': 'border 2px solid'
            }),}   
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_by'].widget = forms.HiddenInput()
        self.fields['ref_no'].widget.attrs['readonly'] = True


# Formulario para el modelo Purchase_invoice
class PurchaseInvoiceForm(forms.ModelForm):
    class Meta:
        model = Purchase_invoice
        fields = '__all__'
        # Configuración de widgets para campos específicos
        widgets = {
            'ref_no': forms.TextInput(attrs={
                'class': 'wd-50 '

            }),
            'observations': forms.Textarea(attrs={
                'class': 'py-10 px-20 '
            }),         
           'total': forms.TextInput(attrs={
                'class': 'field-readonly w-50 px-2'
            }), 
           'tax': forms.TextInput(attrs={
                'class': 'w-50 px-2'
            }),   
           'discount': forms.TextInput(attrs={
                'class': 'w-50 px-2'
            }),
           'to_paid': forms.TextInput(attrs={
                'class': 'w-50 field-readonly'
            }),
           'total_paid': forms.TextInput(attrs={
                'class': 'w-50 field-readonly'
            }),            
            'supplier': forms.Select(attrs={
                'class': 'w-100 select_supplier'
            }),
       

        }
        
    

    def __init__(self, *args, **kwargs):
         # Configuración adicional de campos y etiquetas
        super().__init__(*args, **kwargs)
        self.fields['ref_no'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True
        self.fields['to_paid'].widget.attrs['readonly'] = True
        self.fields['to_paid'].label = _('To paid €')
        self.fields['total_paid'].label = _('Total paid €')
        self.fields['supplier'].label = _('Supplier')
        self.fields['discount'].label = _('Discount €')
        self.fields['total'].label = _('Total €')
        self.fields['tax'].label = _('Taxes %')
        self.fields['is_paid'].label = _('Paid')
        # Filtra las opciones de proveedores para incluir solo proveedores activos
        self.fields['supplier'].queryset = Supplier.supplier.all()

# Formulario para el modelo Purchase_invoice_dtl
class PurchaseInvoiceDtlForms(forms.ModelForm):
    class Meta:
        model = Purchase_invoice_dtl
        fields = '__all__'
        # Configuración de widgets para campos específicos
        widgets = { 
            'product': forms.Select(attrs={
                'class': 'w-100 h-100 px-2 select_product' }),
            'amount': forms.TextInput(attrs={
                'class': 'field-readonly' }), 
            'price': forms.TextInput(attrs={
                'class': 'field-readonly' }),
            'qty': forms.TextInput(attrs={
                'class': 'field-readonly' }),           
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].label = _('Price €')
        self.fields['amount'].widget.attrs['readonly'] = True