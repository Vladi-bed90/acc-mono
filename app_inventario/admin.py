from django.contrib import admin
from .models import ProductoMaster, ProductoVenta, Lote, MovInventario, Inventario

admin.site.register(ProductoMaster)
admin.site.register(ProductoVenta)
admin.site.register(Lote)
admin.site.register(MovInventario)
admin.site.register(Inventario)
