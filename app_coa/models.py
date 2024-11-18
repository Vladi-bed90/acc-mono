from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.utils.timezone import now



class CoaName(models.Model):
    coa_name        = models.CharField(max_length=100)
    is_active       = models.BooleanField(default=True)
    created_by      = models.ForeignKey(User, null=True, default=User ,on_delete=models.CASCADE)
    created_at      = models.DateTimeField(blank=True ,default=now, editable=False)
    
    def __str__(self):
        return self.coa_name
    



class COA(MPTTModel):
    name                = models.CharField(max_length=50)
    number              = models.CharField(max_length=12, null=True, blank=True)
    parent              = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    coa_name            = models.ForeignKey(CoaName, on_delete=models.CASCADE, null=True, blank=True)
    
    es_banco            = models.BooleanField(default=False)
    es_auxiliar         = models.BooleanField(default=False)
    es_centro_de_costos = models.BooleanField(default=False)
    es_sucursal         = models.BooleanField(default=False)
    es_honorarios       = models.BooleanField(default=False)
    
    class MPTTMeta:
        order_insertion_by = ['name']
        
    def __str__(self):
        return f"{self.number} - {self.name}"
