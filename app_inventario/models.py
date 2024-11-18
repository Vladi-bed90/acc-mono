from django.db import models




class ProductoMaster(models.Model):
    """
    Modelo que representa un producto master, de el se crean los productos de venta
    """
    nombre_producto_master = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_producto_master


class ProductoVenta(models.Model):
    nombre_producto_venta = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    sku = models.CharField(max_length=100, blank=True, null=True)

    # Cod Facturacion
    cod_facturacion_cl = models.CharField(max_length=100)
    
    # Producto Master
    producto_master = models.ManyToManyField(ProductoMaster, related_name='productos_venta')
    
    def __str__(self):
        return self.nombre_producto_venta
    

class Lote(models.Model):
    """
    Modelo que representa un lote
    Empieza con el número 10000
    """
    lote = models.SmallIntegerField(unique=True)
    comentario = models.TextField(blank=True, null=True)
    es_importacion = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.lote}"
    
    
class MovInventario(models.Model):
    """
    Modelo que representa un movimiento de inventario
    """
    
    TIPO_MOV = (
        ('ENTRADA', 'ENTRADA'),
        ('SALIDA', 'SALIDA'),
    )
    
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    cantidad = models.PositiveIntegerField()
    producto_master = models.ForeignKey(ProductoMaster, on_delete=models.CASCADE)
    tipo_movimiento = models.CharField(max_length=100, choices=TIPO_MOV, default='SALIDA')
    comentario = models.CharField(max_length=255, blank=True, null=True)
    
    # Se define el lote y el precio unitario, depende si es Entrada o Salida
    # Si es entrada, se define el lote y el precio unitario
    # Si es salida, se busca en Inventario el lote y el precio unitario (FIFO)
    lote = models.ForeignKey(Lote ,null=True, blank=True ,on_delete=models.CASCADE)
    precio_unitario = models.DecimalField(null=True, blank=True ,max_digits=10, decimal_places=2)
    
    # Condicionales
    es_merma = models.BooleanField(default=False)
    es_listo = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.tipo_movimiento} - {self.cantidad} - {self.producto_master.nombre_producto_master}"
    
    
class Inventario(models.Model):
    """
    Modelo que representa el inventario actual, se utiliza el método FIFO
    """
    producto_master = models.ForeignKey(ProductoMaster, on_delete=models.CASCADE)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.producto_master.nombre_producto_master} - {self.cantidad}"