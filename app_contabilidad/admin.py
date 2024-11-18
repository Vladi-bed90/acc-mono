from django.contrib import admin
from .models import Comprobante, RegistroComprobante, TipoDocumentoTributario,\
                    ClienteProveedor, CentroDeCostos, Sucursal, LibroCompra, LibroVenta, \
                    PeriodoContable


class ClienteProveedorAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'rut', 'get_pais_alpha_3')
    list_filter = ('pais',)
    search_fields = ('razon_social__icontains', 'rut__icontains')
    
    # Mostrar Cod Pais Ej: Chile >> CHL
    def get_pais_alpha_3(self, obj):
        return obj.pais.alpha_3

class TipoDocumentoTributarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_documento', 'cod_documento', 'country')
    list_filter = ('country',)
    search_fields = ('nombre_documento',)
    

class PeriodoContableAdmin(admin.ModelAdmin):
    list_display = ('mes', 'anio', 'empresa')
    list_filter = ('mes', 'anio', 'empresa')
    search_fields = ('mes', 'anio')



admin.site.register(ClienteProveedor, ClienteProveedorAdmin)
admin.site.register(CentroDeCostos)
admin.site.register(Sucursal)
admin.site.register(TipoDocumentoTributario, TipoDocumentoTributarioAdmin)
admin.site.register(RegistroComprobante)
admin.site.register(PeriodoContable, PeriodoContableAdmin)


class RegistroComprobanteInline(admin.TabularInline):
    model = RegistroComprobante
    extra = 2
    

@admin.register(LibroVenta)
class LibroVentaAdmin(admin.ModelAdmin):
    readonly_fields = ['id_unico_dte']  

@admin.register(LibroCompra)
class LibroCompraAdmin(admin.ModelAdmin):
    readonly_fields = ['id_unico_dte']    
    
@admin.register(Comprobante)
class ComprobanteAdmin(admin.ModelAdmin):
    readonly_fields = ['suma_debe', 'suma_haber', 'id_unico']
    inlines = [RegistroComprobanteInline,]