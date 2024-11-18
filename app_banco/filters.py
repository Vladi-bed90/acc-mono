from django_filters import FilterSet
from .tables import MovimientoBancarioTable
from .models import MovimientoBancario

class MovimientoBancarioFilter(FilterSet):
    class Meta:
        model = MovimientoBancario
        fields = {"monto": ["exact", "contains"], "descripcion": ["contains"]}
        
        
        
        
## No funcionó la primera vez, si no se arregla ELIMIRAR