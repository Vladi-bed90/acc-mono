from django.db import models
import datetime
from django.db.models import Max

from app_empresa.models import Empresa, Country
from app_coa.models import COA

from django.db.models import F

TIPO_CHOICES = (
    ("I", "INGRESO"),
    ("E", "EGRESO"),
    ("T", "TRASPASO")
    )



class TipoDocumentoTributario(models.Model):
    
    class CountryChoices(models.TextChoices):
        CHILE       = 'CHILE'
        MEXICO      = 'MEXICO'
        COLOMBIA    = 'COLOMBIA'
        USA         = 'USA'
        
        
    cod_documento               = models.CharField(max_length=3) #Ver como se hace con otros paises
    nombre_documento            = models.CharField(max_length=50)
    country                     = models.CharField(max_length=20, choices=CountryChoices.choices, default=CountryChoices.CHILE)
    
    es_activo                   = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.cod_documento} - {self.nombre_documento}"
    

class CentroDeCostos(models.Model):
    
    cc_slug = models.CharField(max_length=4)
    cc_name = models.CharField(max_length=50)
    
    cc_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.cc_slug} - {self.cc_name}"


class Sucursal(models.Model):
    
    suc_slug = models.CharField(max_length=4)
    suc_name = models.CharField(max_length=50)
    
    cc_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.suc_slug} - {self.suc_name}"


class ClienteProveedor(models.Model): #Solo Chile?
    # Datos Generales
    rut =             models.CharField(max_length = 10) # Agregar Unico
    name =            models.CharField(max_length=120, blank = True)
    codigo =          models.CharField(max_length=20, blank = True)
    razon_social =    models.CharField(max_length=120)
    giro =            models.CharField(max_length=120, blank = True)
    tel_number =      models.CharField(max_length=12, blank = True)
    email =           models.EmailField(blank = True)
    
    # Pais
    pais =            models.ForeignKey(Country, default=1, on_delete=models.CASCADE)
    
    # Booleans
    es_activo =       models.BooleanField(default=True)
    es_proveedor =    models.BooleanField(default=False)
    es_cliente =      models.BooleanField(default=False)
    es_extranjero =   models.BooleanField(default=False)

    # Agregar Save() para rut, o hacerlo en FrontEnd

    def __str__(self):
        return f"{self.rut} - {self.razon_social}"
    
    
    
    
    
    

class Comprobante(models.Model):
    numero_comprobante  = models.IntegerField()
    fecha               = models.DateField()
    tipo                = models.CharField(max_length= 20 ,choices=TIPO_CHOICES)
    glosa               = models.CharField(max_length=120 ,blank=True)
    
    # Todos deben ser cuadrados *Obligatorio
    suma_debe           = models.FloatField(default=0, editable=False)
    suma_haber          = models.FloatField(default=0, editable=False)
    es_cuadrado         = models.BooleanField(default=True)
    es_done             = models.BooleanField(default=False)
    
    # Puede generar problemas si se repite el <numero_comprobante> en siguente año
    id_unico            = models.CharField(max_length=50, unique= True)
    
    # Apunta a la empresa
    empresa             = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    
    # Analisis
    day_num             = models.SmallIntegerField(blank=True, null=True, default=0)
    month_num           = models.SmallIntegerField(blank=True, null=True, default=0)
    year_num            = models.SmallIntegerField(blank=True, null=True, default=0)
    
    def save(self, *args, **kwargs):
        
        self.id_unico = f"{self.empresa}-{self.tipo}-{self.numero_comprobante}"
        
        self.day_num = self.fecha.day
        self.month_num = self.fecha.month
        self.year_num = self.fecha.year
        
        if self.suma_debe == self.suma_haber:
            self.es_cuadrado = True
        else:
            self.es_cuadrado = False
                        
        super().save(*args, **kwargs)
        
    
    
    def __str__(self):
        return f"{self.tipo} {self.numero_comprobante}"



class RegistroComprobante(models.Model):
    comprobante             = models.ForeignKey(Comprobante, on_delete=models.CASCADE)
    cuenta_name             = models.ForeignKey(COA,  null=True, blank= True, on_delete=models.CASCADE)
    centro_costo            = models.ForeignKey(CentroDeCostos, null=True, blank= True, on_delete=models.CASCADE)
    sucurasl                = models.ForeignKey(Sucursal, null=True, blank= True, on_delete=models.CASCADE)
    debe                    = models.FloatField(default=0)
    haber                   = models.FloatField(default=0)
    
    # Model <Cliente Proveedor>, Cada Registro puede tener un auxiliar, depende si lo exige
    # Es importante para tener actualizado los saldos de cada auxiliar ("Cta Cte").
    # Tambien debe tener <N° Documento> en caso que estamos "pagando" un documento (DTE) pendiente.
    
    cliente_proveedor       = models.ForeignKey(ClienteProveedor, blank= True, null= True, on_delete=models.SET_NULL)
    numero_documento        = models.IntegerField(blank= True, null= True)
    
    def save(self, *args, **kwargs):
        
        if self.id:
            # Modificacion -->> revisa si existe y hace PUT al valor anterior.
            
            print("already created")
            #Get the current instance
            #instance = self.__class__.objects.get(id=self.pk)
            #print(instance.comprobante, instance.cuenta_name)
            # print what is currently saved in model.
            #print(instance.debe, instance.haber)
            
            # print new value entered by the user.
            #print(self.debe, self.haber)
        else:            
            print("creating")
            #print(self.comprobante_id)
            #Comprobante.objects.filter(id=self.comprobante_id).update(suma_debe = F('suma_debe') + self.debe, suma_haber = F('suma_haber') + self.haber)
            
        
        
                        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.cuenta_name}"
    
    
    
class LibroCompra(models.Model):
    # Informacion DTE
    tipo_documento      = models.ForeignKey(TipoDocumentoTributario, null= True, on_delete=models.SET_NULL) # Ver si poner CASCADE
    folio               = models.IntegerField()
    fecha_documento     = models.DateField()
    proveedor           = models.ForeignKey(ClienteProveedor, on_delete=models.CASCADE)
    monto_exento        = models.FloatField()
    monto_neto          = models.FloatField()
    monto_iva           = models.FloatField()
    monto_total         = models.FloatField()
    detalle             = models.CharField(max_length=120, blank= True, null= True)
    
    # Sirve para hacer match entre registros
    rut_registro        = models.CharField(max_length=50, blank=True)
    
    # Periodo contable
    mes_contable        = models.SmallIntegerField()
    ano_contable        = models.SmallIntegerField()
    
    
    # Contabilidad
    es_cuadrado         = models.BooleanField(default=False)
    empresa             = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    comprobante         = models.ForeignKey(Comprobante, blank=True, null= True, on_delete=models.SET_NULL) # Al eliminar Comprobante no se elimina / REVISAR
    monto_positivo      = models.FloatField(blank=True, default=0)
    es_done             = models.BooleanField(default=False)

    # Conciliacion
    monto_contabilizado = models.FloatField(blank=True, default=0)
    es_anulado          = models.BooleanField(default=False)
    es_pagado           = models.BooleanField(default=False)
    
    id_unico_dte        = models.CharField(max_length=50, unique= True)
    
    def save(self, *args, **kwargs):
        
        # Asigna Id Unico, Proveedor + Tipo Documento + N°Documento, una empresa <<NO>> puede recibir dos documentos iguales!
        if self.id_unico_dte:
            pass
        else:
            self.id_unico_dte = f"{self.proveedor.rut}.{self.tipo_documento.cod_documento}.{self.folio}"
        
             
        
        # Revisa si la suma de los montos cuadra con el total.
        if not self.monto_exento + self.monto_iva + self.monto_neto == self.monto_total:
            self.es_cuadrado = False
        else:
            self.es_cuadrado = True
        
        # Agrega numero comprobante al registro.
        if self.comprobante:
            print("Comprobante Existe")
            
        else:
            # Tipo siempre "T" por naturaleza contable
            tipo = "T" 
            last_num = Comprobante.objects.filter(empresa_id=self.empresa.id ,tipo=tipo, numero_comprobante__gte=2999999, numero_comprobante__lte=3999999).aggregate(Max('numero_comprobante'))
            if last_num['numero_comprobante__max'] == None:
                comprobante_num = 3000000
            else:
                comprobante_num = last_num['numero_comprobante__max'] + 1
                
            self.comprobante = Comprobante.objects.create(
                numero_comprobante = comprobante_num,
                fecha = self.fecha_documento,
                tipo = tipo,
                empresa = self.empresa,
                glosa = f"Folio:{self.folio} - {self.detalle}"
            )
        
        # Agrega rut para info apoyo (ej: 25.455.302-6 --> 254553026)
        if self.rut_registro:
            pass
        else:
            try:
                self.rut_registro = self.proveedor.rut.replace("-", "")
            except:
                pass
        
        # Agrega Monto Positivo para contabilidad        
        if self.monto_positivo == 0:
            self.monto_positivo = abs(self.monto_total)
            
        # Revisa si el Documento esta Pagado
        if self.monto_contabilizado == self.monto_total:
            self.es_pagado = True
        else:
            self.es_pagado = False
            
                 
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.folio} - {self.proveedor}"



class LibroVenta(models.Model):
    # Informacion DTE
    tipo_documento      = models.ForeignKey(TipoDocumentoTributario, null= True, on_delete=models.SET_NULL) # Ver si poner CASCADE
    folio               = models.IntegerField()
    fecha_documento     = models.DateField()
    proveedor           = models.ForeignKey(ClienteProveedor, on_delete=models.CASCADE)
    monto_exento        = models.FloatField()
    monto_neto          = models.FloatField()
    monto_iva           = models.FloatField()
    monto_total         = models.FloatField()
    detalle             = models.CharField(max_length=120, blank= True, null= True)
    
    # Sirve para hacer match entre registros
    rut_registro        = models.CharField(max_length=50, blank=True)
    
    # Periodo contable
    mes_contable        = models.SmallIntegerField()
    ano_contable        = models.SmallIntegerField()
    
    
    # Contabilidad
    es_cuadrado         = models.BooleanField(default=False)
    empresa             = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    comprobante         = models.ForeignKey(Comprobante, blank=True, null= True, on_delete=models.SET_NULL) # Al eliminar Comprobante no se elimina / REVISAR
    monto_positivo      = models.FloatField(blank=True, default=0)
    es_done             = models.BooleanField(default=False)

    # Conciliacion
    monto_contabilizado = models.FloatField(blank=True, default=0)
    es_anulado          = models.BooleanField(default=False)
    es_pagado           = models.BooleanField(default=False)
    
    
    id_unico_dte        = models.CharField(max_length=50, unique= True)
    
    def save(self, *args, **kwargs):
        
        # Asigna Id Unico, Proveedor + Tipo Documento + N°Documento, una empresa <<NO>> puede recibir dos documentos iguales!
        if self.id_unico_dte:
            pass
        else:
            self.id_unico_dte = f"{self.empresa.rut}.{self.tipo_documento.cod_documento}.{self.folio}"
        
        # Revisa si la suma de los montos cuadra con el total.
        if not self.monto_exento + self.monto_iva + self.monto_neto == self.monto_total:
            self.es_cuadrado = False
        else:
            self.es_cuadrado = True
        
        # Agrega numero comprobante al registro.
        if self.comprobante:
            print("Comprobante Existe")
            
        else:
            # Tipo siempre "T" por naturaleza contable
            tipo = "T" 
            last_num = Comprobante.objects.filter(empresa_id=self.empresa.id ,tipo=tipo, numero_comprobante__gte=3999999, numero_comprobante__lte=5000000).aggregate(Max('numero_comprobante'))
            if last_num['numero_comprobante__max'] == None:
                comprobante_num = 4000000
            else:
                comprobante_num = last_num['numero_comprobante__max'] + 1
                
            self.comprobante = Comprobante.objects.create(
                numero_comprobante = comprobante_num,
                fecha = self.fecha_documento,
                tipo = tipo,
                empresa = self.empresa,
                glosa = f"Folio:{self.folio} - {self.detalle}"
            )
        
        # Agrega rut para info apoyo (ej: 25.455.302-6 --> 254553026)
        if self.rut_registro:
            pass
        else:
            try:
                self.rut_registro = self.proveedor.rut.replace("-", "")
            except:
                pass
        
        # Agrega Monto Positivo para contabilidad        
        if self.monto_positivo == 0:
            self.monto_positivo = abs(self.monto_total)
            
        # Revisa si el Documento esta Pagado
        if self.monto_contabilizado == self.monto_total:
            self.es_pagado = True
        else:
            self.es_pagado = False
            
                 
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.folio} - {self.proveedor}"    
    
    
    
class PeriodoContable(models.Model):
    mes = models.SmallIntegerField()
    anio = models.SmallIntegerField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    es_cerrado = models.BooleanField(default=False)
    
    total_iva_credito = models.FloatField(default=0)
    total_iva_debito = models.FloatField(default=0)
    
    
    def __str__(self):
        return f"{self.mes}/{self.anio} - {self.empresa}"