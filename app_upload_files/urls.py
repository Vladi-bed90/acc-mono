from django.urls import path
from .views import upload_cartola_generica, upload_index, upload_libro_compras_chile, upload_libro_ventas_chile


urlpatterns = [
    path('', upload_index, name= 'upload-index'),
    path('upload_cartola_generica/', upload_cartola_generica, name='upload-cartola-generica'),
    path('upload_libro_compras_chile/', upload_libro_compras_chile, name= 'upload-libro-compras-chile'),
    path('upload_libro_ventas_chile/', upload_libro_ventas_chile, name= 'upload-libro-ventas-chile'),
]