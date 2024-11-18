from django import forms
from .models import MovimientoBancario, MedioDePago


class MovimientoBancarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoBancario
        fields = (
            'fecha',
            'monto',
            'descripcion',
            'cargo_abono',
            'detalle_adicional',
            'banco',
            'medio_de_pago'
        )
        
        
class MedioDePagoForm(forms.ModelForm):
    class Meta:
        model = MovimientoBancario
        fields = ('medio_de_pago',)
        widgets = {
            'medio_de_pago': forms.Select(attrs={'class': 'form-control'})
            }
        labels = {'medio_de_pago':''}