from django.urls import path
# Views Contabilidad
from .views import get_info_contable, get_libro_compras, get_detalle_compra, get_libro_ventas, magic_libro_ventas
# Views Comprobante
from .views import comprobante_list, contabilizar_comprobante, add_registro, get_info_cuenta_contable, add_comprobante, add_auxiliar
# Views Impuestos
from .views import get_index_tax




urlpatterns = [
    path('', get_info_contable, name= 'get-info-contable'),
    path('add-auxiliar/', add_auxiliar, name= 'add-auxiliar'),
    path('comprobantes/', comprobante_list, name='all-comprobantes'),
    path('comprobantes/add/', add_comprobante, name= 'add-comprobante'),
    path('comprobantes/get_coa/', get_info_cuenta_contable, name= 'get-info-cuenta-contable'),
    path('comprobantes/<int:pk>/', contabilizar_comprobante, name= 'contabilizar-comprobante'),
    path('comprobantes/<int:pk>/add_registro/', add_registro, name= 'add-registro'),
    path('libro_compras/', get_libro_compras, name= 'get-libro-compras'),
    path('libro_compras/<int:compra_pk>/', get_detalle_compra, name= 'get-detalle-compra'),
    path('libro_compras/<int:compra_pk>/edit_form/', get_detalle_compra, name= 'get-detalle-compra-edit-form'),
    path('libro_ventas/', get_libro_ventas, name= 'get-libro-ventas'),
    path('libro_ventas/magic/', magic_libro_ventas, name= 'magic-libro-ventas'),
    path('tax/', get_index_tax, name= 'get-index-tax'),

]
