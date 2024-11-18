from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
import datetime
from django.db.models import Max

from app_empresa.models import Empresa, Country, Currency
from app_contabilidad.models import Comprobante


MOV_CHOICES = (("C", "C"), ("A", "A"))

class MedioDePago(models.Model):
    name            = models.CharField(max_length=120)
    mp_code2        = models.CharField(max_length=2, default="")
    url             = models.URLField(max_length=200, blank=True)
    country         = models.ForeignKey(Country, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'medio de pago'
        verbose_name_plural = 'medio de pago'
    
    def __str__(self):
        return f"{self.country.alpha_2} :. {self.name}"




class Banco(models.Model):
       
    name            = models.CharField(max_length=50)  
    numero_cuenta   = models.CharField(max_length=50, blank = True)
    tipo_cuenta     = models.CharField(max_length=50, blank = True)
    empresa         = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    currency        = models.ForeignKey(Currency, on_delete=models.CASCADE)
    #banco_img       = models.ImageField() PENDIENTE
    
    class Meta:
        verbose_name = 'banco'
        verbose_name_plural = 'banco'
    
    def __str__(self):
        return f"{self.empresa.country}: {self.name}"
    
    
    
    

class MovimientoBancario(models.Model):
    fecha               = models.DateField()
    monto               = models.FloatField()
    descripcion         = models.CharField(max_length=150)
    cargo_abono         = models.CharField(max_length=1, choices=MOV_CHOICES)
    detalle_adicional   = models.CharField(max_length=150, blank= True)
    banco               = models.ForeignKey(Banco, on_delete=models.CASCADE)
    
    uploaded_by         = models.ForeignKey(User, null=True, default=User ,on_delete=models.CASCADE)
    created_at          = models.DateTimeField(blank=True ,default=now, editable=False)
    
    # Conciliacion
    medio_de_pago       = models.ForeignKey(MedioDePago, default="", blank=True, null=True, on_delete=models.CASCADE)
    rut_chile           = models.CharField(max_length=50 ,blank= True)
    
    # Contabilidad
    monto_positivo      = models.FloatField(blank=True, null=True, default=1)
    comprobante         = models.ForeignKey(Comprobante, blank=True, null= True, on_delete=models.SET_NULL)
    monto_contabilizado = models.FloatField(blank=True, null=True, default=0)
    esta_contabilizado  = models.BooleanField(default=False)
    
    # Analisis
    day_num             = models.SmallIntegerField(blank=True, null=True, default=0)
    month_num           = models.SmallIntegerField(blank=True, null=True, default=0)
    year_num            = models.SmallIntegerField(blank=True, null=True, default=0)
    
    
    def save(self, *args, **kwargs):
        
        if self.comprobante:
            print("Comprobante Existe")
            
        else:
            print("Comprobante No Existe")
            var = ""
            if self.monto > 0:
                var = "I"
            else:
                var = "E"
            
            # Buscando último número del comprobante. (por tipo I/E/T en este caso <var>)
            last_num = Comprobante.objects.filter(tipo=var, numero_comprobante__gte=999999, numero_comprobante__lte=2000000).aggregate(Max('numero_comprobante'))
            if last_num['numero_comprobante__max'] == None:
                comprobante_num = 1000000
            else:
                comprobante_num = last_num['numero_comprobante__max'] + 1
            
            # Creando Comprobante    
            self.comprobante = Comprobante.objects.create(
                numero_comprobante = comprobante_num,
                fecha = self.fecha,
                empresa = self.banco.empresa,
                tipo = var,
                glosa = f"{self.descripcion} - {self.detalle_adicional}"
            )
            
            # Revisa si el pais es Chile
            if self.banco.empresa.country.alpha_2 == "CL":
                print("REVISANDO RUT")
                # Caso Cobro
                if self.cargo_abono == "C":
                    var = self.descripcion
                    rut = var.replace(".", "").replace("-", "").split(" ")[-1]
                    # Revisa "K" en el rut
                    if rut[-1].upper() == "K":
                        self.rut_chile = rut.upper()
                    else:
                        try:
                            self.rut_chile = str(int(rut))
                        except:
                            self.rut_chile = str(rut)
                            
                # Caso Abono
                elif self.cargo_abono == "A":
                    var = self.descripcion
                    rut = var.replace(".", "").replace("-", "").split(" ")[0]
                    # Revisa "K" en el rut
                    if rut[-1].upper() == "K":
                        self.rut_chile = rut.upper()
                    else:
                        try:
                            self.rut_chile = str(int(rut))
                        except:
                            self.rut_chile = str(rut)
                
                else:
                    pass
        
        self.monto_positivo = abs(self.monto)
        self.day_num = self.fecha.day
        self.month_num = self.fecha.month
        self.year_num = self.fecha.year
                        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'movimiento_bancario'
        verbose_name_plural = 'movimiento_bancario'
        
        
    def __str__(self):
        return f"$ {self.monto} - {self.banco}"