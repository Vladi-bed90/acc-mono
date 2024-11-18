from django.contrib import admin
from .models import Banco, MovimientoBancario, MedioDePago


admin.site.register(Banco)
admin.site.register(MovimientoBancario)
admin.site.register(MedioDePago)
