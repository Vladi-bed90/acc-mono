from django.urls import path
from .views import get_mov_banco, get_resumen_banco, get_lista_banco, get_mov_detalle, get_mov_detalle_form, get_info_apoyo_mov, modificar_medio_de_pago, auto_contabilizacion_abono



urlpatterns = [
    path('', get_lista_banco, name= 'get-info-banco'),
    path('<int:banco_id>', get_resumen_banco, name= 'get-resumen-banco'),
    path('<int:banco_id>/mov/', get_mov_banco, name= 'get-mov-banco'),
    path('<int:banco_id>/mov/magic/', auto_contabilizacion_abono, name= 'auto-contabilizacion-abono'),
    path('<int:banco_id>/mov/<int:mov_id>', get_mov_detalle, name= 'get-mov-detalle'),
    path('<int:banco_id>/mov/<int:mov_id>/info_apoyo/', get_info_apoyo_mov, name= 'get-info-apoyo-mov'),
    path('<int:banco_id>/mov/<int:mov_id>/form', get_mov_detalle_form, name= 'get-mov-detalle-form'),
    path('<int:banco_id>/mov/<int:mov_id>/modificar_medio_de_pago', modificar_medio_de_pago, name= 'modificar-medio-de-pago'),
]
