from django.contrib import admin
from .models import UploadCartolaBanco, UploadComprasChile, UploadVentasChile



admin.site.register(UploadCartolaBanco)
admin.site.register(UploadComprasChile)
admin.site.register(UploadVentasChile)

