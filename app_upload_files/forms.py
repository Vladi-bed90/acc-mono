from django import forms
from .models import UploadCartolaBanco, UploadComprasChile, UploadVentasChile




# Cartola Generica
class UploadCartolaBancoForm(forms.ModelForm):
    class Meta:
        model = UploadCartolaBanco
        fields = ('file_name',)
        
        
# Compras Chile
class UploadComprasChileForm(forms.ModelForm):
    class Meta:
        model = UploadComprasChile
        fields = ('file_name',)
        
        
# Ventas Chile
class UploadVentasChileForm(forms.ModelForm):
    class Meta:
        model = UploadVentasChile
        fields = ('file_name',)