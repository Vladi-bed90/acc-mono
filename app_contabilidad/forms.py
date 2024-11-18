from django import forms
from .models import RegistroComprobante, Comprobante, LibroCompra, ClienteProveedor
from django.db.models import F

from .fields import ListTextWidget


class DateInput(forms.DateInput):
    input_type = 'date'



class RegistroComprobanteForm(forms.ModelForm):
    # Filter > Solo 'Leaf' cuentas
    def __init__(self , *args, **kwargs):
        super(RegistroComprobanteForm, self).__init__(*args, **kwargs)

        self.fields['cuenta_name'].queryset = self.fields['cuenta_name'].queryset.filter(rght=F('lft')+1)
        self.fields["comprobante"].disabled = False
        #self.fields["cliente_proveedor"].queryset = self.fields["cliente_proveedor"].queryset.filter(pais=empresa)
        #self.fields["sucurasl"].queryset = self.fields["sucurasl"].queryset.filter(cc_empresa=self.empresa)
        
        # Opcion con Datalist - Tiene problema con POST, llega el STR de la cuenta y genera error
        """self.fields['cuenta_name'].widget = ListTextWidget(data_list=self.fields['cuenta_name'].queryset.filter(rght=F('lft')+1),#.values_list('name'),
                                                           name='country-list',
                                                           attrs={
                                                               'class': 'form-control form-control-sm',
                                                               'coa_id': self.instance.pk
                                                           })"""
    
    class Meta:
        model = RegistroComprobante
        fields = (
            'comprobante',
            'cuenta_name',
            'centro_costo',
            'sucurasl',
            'debe',
            'haber',
            'cliente_proveedor',
            'numero_documento'
        )
        widgets = {
            'cuenta_name': forms.Select(attrs={
                'id': 'cuenta_id',
                'class': 'form-select form-select-sm',
                'name': 'cuenta_name',
                }),
            'centro_costo': forms.Select(attrs={'class': 'form-select form-select-sm',
                                                'readonly': True,
                                                'style': 'background: black',
                                                }),
            'sucurasl': forms.Select(attrs={'class': 'form-select form-select-sm',
                                            'readonly': True,
                                            'style': 'background: black',
                                            }),
            
            'debe': forms.TextInput(attrs={
                'id': 'form_debe',
                'last_value': 0,
                'class': 'form-control text-center form-control-sm',
                'style': 'width:20ch',
                'min': 0,
                '_': "on change if (value of me) is not empty set x to (value of me) as an Int then set y to #total_debe.value as an Int then set z to @value as an Int then set diff to (x - z) then put (diff + y) into #total_debe then set @value to x end",
                }),
            'haber': forms.TextInput(attrs={
                'id': 'form_haber',
                'last_value': 0,
                'class': 'form-control text-center form-control-sm',
                'style': 'width:20ch',
                'min': 0,
                '_': "on change if (value of me) is not empty set x to (value of me) as an Int then set y to #total_haber.value as an Int then set z to @value as an Int then set diff to (x - z) then put (diff + y) into #total_haber then set @value to x end",               
                }),
            'cliente_proveedor': forms.Select(attrs={'class': 'form-select form-select-sm',
                                            'readonly': True,
                                            'style': 'background: black',
                                            }),
            'numero_documento': forms.TextInput(attrs={
                                            'class': 'form-control form-control-sm',
                                            'id':'numero_documento',
                                            'readonly': True,
                                            'style': 'background: black',
                                            }),            
            }
        
        
class ComprobanteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ComprobanteForm, self).__init__(*args, **kwargs)
        self.fields["numero_comprobante"].disabled = False
        self.fields["tipo"].disabled = False
    class Meta:
        model = Comprobante
        fields = (
            'numero_comprobante',
            'fecha',
            'tipo',
            'glosa'
        )
        
        widgets = {
            'numero_comprobante': forms.NumberInput(attrs={'class': 'form-control', 'required': False}),
            
            'fecha':              DateInput(attrs={'class': 'form-control', 'required': False}),
                               
            'tipo':               forms.Select(
                attrs={'class': 'form-control',
                       'placeholder': 'Tipo',
                       'required': True,
                       }),
            'glosa':              forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Leave a comment here',
                       }),
            
            }

        
class LibroCompraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LibroCompraForm, self).__init__(*args, **kwargs)
        self.fields["folio"].disabled = False
        self.fields["proveedor"].disabled = False
    class Meta:
        model = LibroCompra
        fields = (
            'empresa',
            'tipo_documento',
            'folio',
            'fecha_documento',
            'proveedor',
            'monto_exento',
            'monto_neto',
            'monto_iva',
            'monto_total',
            'detalle',
        )
        widgets = {
            'empresa': forms.Select(attrs={'class': 'form-control form-control-sm',}),
            'tipo_documento': forms.Select(attrs={'class': 'form-control form-control-sm',}),
            'folio': forms.NumberInput(attrs={'class': 'form-control form-control-sm fw-bolder',}),
            'fecha_documento': DateInput(attrs={'class': 'form-control form-control-sm',}),
            'proveedor': forms.Select(attrs={'class': 'form-control form-control-sm',}),
            'monto_exento': forms.NumberInput(attrs={'class': 'form-control form-control-sm',}),
            'monto_neto': forms.NumberInput(attrs={'class': 'form-control form-control-sm',}),
            'monto_iva': forms.NumberInput(attrs={'class': 'form-control form-control-sm',}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control form-control-sm',}),
            'detalle': forms.TextInput(attrs={'class': 'form-control form-control-sm',}),
        }
        
 
class ContabilizarCompraRapidoForm(forms.ModelForm):
    pass
 
 
 
class AgregarAuxiliarForm(forms.ModelForm):
    class Meta:
        model = ClienteProveedor
        fields = ('rut',
                  'razon_social',
                  ) 
        widgets = {
            'rut': forms.TextInput(attrs={'class':'form-control form-control-sm','placeholder':'Ej: 12345678-9', 'pattern': '^(\d{7,8}-[\dkK])$'}),
            'razon_social': forms.TextInput(attrs={'class':'form-control form-control-sm','placeholder':'Ej: SHALOM SPA'}),
        }
 
        
# TEST IGNORE
class FormForm(forms.Form):
   char_field_with_list = forms.CharField(required=True)

   def __init__(self, *args, **kwargs):
        _country_list = kwargs.pop('data_list', None)
        super(FormForm, self).__init__(*args, **kwargs)

        # the "name" parameter will allow you to use the same widget more than once in the same
        # form, not setting this parameter differently will cuse all inputs display the
        # same list.
        self.fields['char_field_with_list'].widget = ListTextWidget(data_list=_country_list, name='country-list')