from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Standard Libraries
import random
import string
# App COA
from app_coa.models import CoaName, COA



class Country(models.Model):
    # https://www.iban.com/country-codes
    # This is a complete list of all country ISO codes as described in the ISO 3166 international standard.
    name            = models.CharField(max_length=120)
    alpha_2         = models.CharField(max_length=2)
    alpha_3         = models.CharField(max_length=3)
    country_code    = models.CharField(max_length=3)
    #country_flag    = models.ImageField() PENDIENTE
    
    def __str__(self):
        return f"{self.alpha_3} - {self.name}"
    
    
class Currency(models.Model):
    # https://www.iban.com/currency-codes
    country         = models.ForeignKey(Country, on_delete=models.CASCADE)
    cur_name        = models.CharField(max_length=120)
    cur_code        = models.CharField(max_length=3)
    
    def __str__(self):
        return f"{self.cur_code}: {self.country.name}"





class DefaultCuentasContablesEmpresa(models.Model):
    
    """
    Objetivo: Tener cuentas contables definidas con anticipacion, para facilitar la clasificacion de hechos contables
              en el futuro con eficiencia.
              
              Por ejemplo: En el <Libro de Ventas> el trabajo es bastante repetitivo, por lo tanto podemos observar 
              los comportamientos comunes y crear estos <Ajustes> para automatizar el proceso (con boton puede ser una opcion).
              
    """
    name                    = models.CharField(max_length=100)
    
    # Banco
    default_banco           = models.ForeignKey(COA, blank=True, null=True ,related_name='default_banco' ,on_delete=models.CASCADE)
    
    
    # Compras
    default_compras         = models.ForeignKey(COA, blank=True, null=True ,related_name='default_compras' ,on_delete=models.CASCADE)
    default_iva_compras     = models.ForeignKey(COA, blank=True, null=True ,related_name='default_iva_compras' ,on_delete=models.CASCADE)
    
    # Ventas
    default_ventas          = models.ForeignKey(COA, blank=True, null=True ,related_name='default_ventas' ,on_delete=models.CASCADE)
    default_iva_ventas      = models.ForeignKey(COA, blank=True, null=True ,related_name='default_iva_ventas' ,on_delete=models.CASCADE)
    
    # Honorarios
    default_honorarios      = models.ForeignKey(COA, blank=True, null=True ,related_name='default_honorarios' ,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"




class Empresa(models.Model):

    nombre                           = models.CharField(max_length=100)
    rut                              = models.CharField(max_length=20)
    razon_social                     = models.CharField(max_length=100, blank=True, default="")
    country                          = models.ForeignKey(Country, on_delete=models.CASCADE)
    #currency        = models.ForeignKey(Currency, on_delete=models.CASCADE)
    
    random_short_uuid                = models.CharField(max_length=8, blank=True, unique=True)
    
    # Contabilidad
    #
    #   hay que agregar Info General, donde se elige --> COA, y otros datos
    #   Puede ser en otro modelo
    
    plan_de_cuentas                  = models.ForeignKey(CoaName, blank=True, on_delete=models.CASCADE)
    afecta_iva                       = models.BooleanField(default=True)
    
    # Ajustes Generales
    def_cuentas_contables_activated  = models.BooleanField(default=False)
    def_cuentas_contables            = models.ForeignKey(DefaultCuentasContablesEmpresa, blank=True, null=True, on_delete=models.CASCADE)
    
    created_by                       = models.ForeignKey(User, null=True, default=User ,on_delete=models.CASCADE)
    created_at                       = models.DateTimeField(blank=True ,default=now, editable=False)
    
    def save(self, *args, **kwargs):
        
        if self.random_short_uuid:
            pass
        else:
            # Select 4 digits at random
            digits = random.choices(string.digits, k=4)
            
            # Select 4 Uppercase letters at random
            letters = random.choices(string.ascii_uppercase, k=4)
            
            #Shuffle both letters + digits
            sample = random.sample(digits + letters, 8)
            uuid = ''.join(sample)
            
            self.random_short_uuid = uuid
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nombre}"




    