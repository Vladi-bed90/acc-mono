from django.urls import path
from .views import get_lista_empresas, get_empresa_homepage


urlpatterns = [
    path('', get_lista_empresas, name= 'get-lista-empresas'),
    path('<str:empresa>/', get_empresa_homepage, name= 'empresa-homepage'),
]
