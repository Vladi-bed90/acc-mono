from django_filters import FilterSet, filters
from .models import LibroCompra

class LibroCompraFilter(FilterSet): 
    class Meta:
        model = LibroCompra
        fields = {"mes_contable": ["exact",], "ano_contable": ["exact",]}