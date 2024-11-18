from django.shortcuts import render
from .models import Empresa



def get_lista_empresas(request):

    data = Empresa.objects.all()
    context = {'data': data}
    
    return render(request, 'home.html', context)
    
    
    
def get_empresa_homepage(request, empresa):
    
    data_empresa = {}#Empresa.objects.get(random_short_uuid=empresa)
    context = {'data_empresa':data_empresa, 'empresa':empresa}
    
    return render(request, 'empresa_homepage.html', context)
        
