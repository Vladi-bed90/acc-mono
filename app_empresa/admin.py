from django.contrib import admin
from .models import Empresa, Country, Currency, DefaultCuentasContablesEmpresa

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'alpha_2', 'alpha_3', 'country_code',)
    #list_editable = ("alpha_2",)
    
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('cur_code', 'cur_name', 'country',)

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'country',)
    list_filter = ('nombre',)
    search_fields = ['nombre__icontains',]

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(DefaultCuentasContablesEmpresa)

