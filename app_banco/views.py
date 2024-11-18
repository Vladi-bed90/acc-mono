from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Q, Sum
from datetime import datetime
# App Empresa
from app_empresa.models import Empresa
# App Banco
from .models import MovimientoBancario, Banco
from .forms import MovimientoBancarioForm, MedioDePagoForm
# App Contabilidad
from app_contabilidad.models import LibroCompra, LibroVenta, RegistroComprobante, Comprobante
# App Upload Files
from app_upload_files.forms import UploadCartolaBancoForm
from app_upload_files.views import upload_cartola_generica
# Filters
from .filters import MovimientoBancarioFilter
# Tables
from .tables import MovimientoBancarioTable
from django_tables2 import RequestConfig

# Plotly Charts
import plotly.express as px



@login_required
def get_lista_banco(request, empresa):
    bancos = Banco.objects.filter(empresa__random_short_uuid=empresa)
    context = {'bancos':bancos, 'empresa':empresa} #https://stackoverflow.com/questions/45547674/how-to-execute-a-group-by-count-or-sum-in-django-orm
    
    return render(request, 'info_banco.html', context)


@login_required
def get_resumen_banco(request, empresa, banco_id):
    
    #print(empresa, banco_id)
    
    #del request.session['idempresa']
    data = MovimientoBancario.objects.filter(
        banco__empresa__random_short_uuid=empresa,banco_id=banco_id).values('banco','banco__name','month_num').order_by('banco','month_num').annotate(Saldo=Sum('monto'))
    
    context = {'data': data, 
               'empresa': empresa, 
               'banco': banco_id,
               #'chart': mov_banco_chart(empresa=empresa, banco_id=banco_id),
               #'comp_abono_cargo_chart': comp_abono_cargo_chart(empresa=empresa, banco_id=banco_id),
               #'detalle_abonos_chart': detalle_abonos_chart(empresa=empresa, banco_id=banco_id),
               }
    
    return render(request, 'resumen_banco.html', context)


@login_required
def get_mov_banco(request, empresa, banco_id):
    
    # Date Variables
    today = datetime.today()
    mes = today.month
    anio = today.year    
    anio_options = [anio, anio-1, anio-2]
    mes_options = [1,2,3,4,5,6,7,8,9,10,11,12]
    
    if request.method == "POST":
        upload_cartola_generica(request)
        return HttpResponse(status=200)
     
    if request.method == "GET":
        
        # Filtros Navbar  
        base_filter =  Q(banco__empresa__random_short_uuid=empresa) & Q(banco_id=banco_id)
        if request.GET.get('mes'):
            mes = int(request.GET.get('mes'))
            anio = int(request.GET.get('anio'))
            base_filter = base_filter & Q(month_num=mes) & Q(year_num=anio)
        if not request.GET.get('mes'):
            base_filter = base_filter & Q(month_num=mes) & Q(year_num=anio)
        if request.GET.get('tipo'):
            base_filter = base_filter & Q(cargo_abono=request.GET.get('tipo'))
        #print(base_filter)
        
        table = MovimientoBancarioTable(MovimientoBancario.objects.filter(base_filter))
    
    # Datos Generales
    data_empresa = Empresa.objects.get(random_short_uuid=empresa)
    banco = Banco.objects.get(pk=banco_id)
    # Django-tables2 Settings
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page",1), per_page=15)  
        
    context = {'table': table,
               'data_banco':banco,
               'empresa': empresa,
               'banco':banco_id,
               'data_empresa': data_empresa,
               'mes': mes,
               'anio': anio,
               'anio_options': anio_options,
               'mes_options': mes_options,
               'upload_cartola_banco_form':UploadCartolaBancoForm(),
               }
    
    return render(request, 'mov_banco.html', context)


@login_required
def get_mov_detalle(request, empresa, banco_id, mov_id):
    
    banco = Banco.objects.get(pk=banco_id)
    detalle_mov = MovimientoBancario.objects.get(pk=mov_id)
    
    context = {'detalle_mov': detalle_mov, 'banco':banco, 'empresa': empresa}
    
    return render(request, 'mov_detalle.html', context)


@login_required
def get_mov_detalle_form(request, empresa, banco_id, mov_id):
    
    if request.method == "GET":
        print("GET")
        mov = MovimientoBancario.objects.get(pk=mov_id)
        form = MovimientoBancarioForm(instance=mov)
        
        context = {'form': form, 'empresa':empresa, 'banco':banco_id, 'mov_id':mov_id}
        print(context)
        return render(request, 'partials/mov_detalle_form.html', context)

    if request.method == "POST":
        print("POST")
        mov = MovimientoBancario.objects.get(pk=mov_id)
        form = MovimientoBancarioForm(request.POST, instance=mov)
        if form.is_valid():
            print("FORM VALID")
            form.save()
        
        context = {}

        return HttpResponse('<p>Gracias</p>')
    

# EN PROGRESO
# Para mejor proceso de clasificación
# 15-09/2023 se agregó filtro por tipo (compra, venta,)
@login_required    
def get_info_apoyo_mov(request, empresa, banco_id, mov_id):
    
    mov = MovimientoBancario.objects.get(pk=mov_id)
    tipo = mov.cargo_abono
    # Si el Movimiento bancario es <Cargo> buscamos info de Compras, Remuneraciones, BBHH, Etc
    if tipo == "C":
        compras = LibroCompra.objects.filter(Q(rut_registro=mov.rut_chile) | Q(monto_total=mov.monto_positivo)).values()
        context = {
            'empresa': empresa,
            'compras': compras,
            'tipo': tipo,
            'mov': mov
        }
        
    elif tipo == "A":
        ventas = LibroVenta.objects.filter(Q(rut_registro=mov.rut_chile) | Q(monto_total=mov.monto_positivo)).values()
        context = {
            'empresa': empresa,
            'ventas': ventas,
            'tipo': tipo,
            'mov': mov
        }
    #print(mov.monto_positivo)
    #print(len(compras))
    #context = {'compras':compras}
    
    return render(request, 'partials/mov_detalle_info_apoyo.html', context)


# Objetivo: Saber a que corresponde cada Abono en el banco
# Sirve para luego conciliar el banco
@login_required
def modificar_medio_de_pago(request, empresa, banco_id, mov_id):
    mov = MovimientoBancario.objects.get(pk=mov_id)
    
    if request.method == "GET":
        print("GET") 
        form = MedioDePagoForm(instance=mov)    
        context = {
            'form': form,
            'empresa': empresa,
            'banco_id': banco_id,
            'mov_id': mov_id,
            }
    
        return render(request, 'partials/modificar_medio_de_pago.html', context)
    
    if request.method == "POST":
        print("POST")
        nuevo_mp = request.POST.get('medio_de_pago')
        MovimientoBancario.objects.filter(pk=mov_id).update(medio_de_pago=nuevo_mp)
        mov = MovimientoBancario.objects.get(pk=mov_id)
        context = {
            'empresa': empresa,
            'banco_id': banco_id,
            'mov_id': mov_id,
            'mov': mov
            }
        return render(request, 'partials/medio_de_pago_modificado.html', context)
    


#_____________________________________________________ Helpers _________________________________________________________#

# Se clasifica <Abonos> con cierto patron (Hay que ver por banco, dejar como otra tabla o algo)
# Porque cada banco tiene diferentes <Descripcion> del movimiento.
# En este caso lo aplicamos a Banco Santander - Office Banking, luego vemos como aplicamos en general.

def auto_clasificacion_medio_de_pago(request, empresa, banco_id):
    mov = MovimientoBancario.objects.filter(banco__empresa_random_short_uuid = empresa, 
                                            banco_id = banco_id, 
                                            cargo_abono = 'A',
                                            medio_de_pago__isnull=True)
    
    print(mov)
    pass
    
    

"""
    Se trata de **Contabilizar** los ABONOS que corresponden a pagos por ventas,
    Se filtra los movimientos bancarios por los pendientes de clasificar,
    Luego se busca la cuenta contable de este tipo de pago (Cuenta por cobrar)
    
    -No se utiliza auxiliares por medio de pago, para tener el proceso más SIMPLE
        Decisión totalmente libre por cada empresa >> De hecho se puede pensar de un filtro 
        o agregar en los datos de la empresa, ajuste que corresponde a eso.
        
        
    FALTA:
        -Identificar o crear tabla de Medio de Pago >> Cuenta Contable. Donde se identifica
         la cuenta en forma automatica y la **Contabiliza** en forma mas eficiente.    
"""
def auto_contabilizacion_abono(request, empresa, banco_id):
    # Todos los movimientos por Contabilizar Pendientes
    mov = MovimientoBancario.objects.filter(banco__empresa__random_short_uuid = empresa, 
                                            banco_id = banco_id, 
                                            cargo_abono = 'A',
                                            medio_de_pago__isnull=False,
                                            comprobante__es_done=False).exclude(medio_de_pago__name='Otro')
    
    default_cuentas_contables = Empresa.objects.get(random_short_uuid=empresa)
    default_ventas = default_cuentas_contables.def_cuentas_contables.default_ventas.id
    default_banco = default_cuentas_contables.def_cuentas_contables.default_banco.id
    
    rango = mov.count()
    print(rango)
    
    # Revisa si hay registros Pendientes
    if rango == 0:
        pass
    else:
        for i in range(rango):
            print(i, mov.count())
            with transaction.atomic():
                # VARIABLES
                """
                    Se utiliza mov[0] porque al parecer que cada Loop se ELIMINA el registro de la lista,
                    por eso se ocupa el primer registro (como es el 'siguiente'). 
                """
                comprobante = mov[0].comprobante
                comprobante_id = mov[0].comprobante.id
                monto_positivo_mov = mov[0].monto_positivo
                
                # DEBE
                RegistroComprobante.objects.create(comprobante=comprobante,
                                                cuenta_name_id = default_banco,
                                                debe=monto_positivo_mov,
                                                haber=0)
                # HABER
                RegistroComprobante.objects.create(comprobante=comprobante,
                                                cuenta_name_id = default_ventas,
                                                debe=0,
                                                haber=monto_positivo_mov)
                
                if comprobante.es_done == False:
                    print(comprobante)
                    print("FALSE")
                    comprobante.es_done=True
                    print(comprobante.es_done)
                    comprobante.save()
                    print("AFTER SAVE")
                    
    
    
   
    return HttpResponse(status = 200)










#_____________________________________________________ END Helpers _____________________________________________________#
    
#_____________________________________________________ Plotly Charts _____________________________________________________#


@login_required
def test_chart(request):
    mov = MovimientoBancario.objects.filter(
        banco__empresa_id=1,banco_id=1).values('banco','banco__name','fecha').order_by('banco','fecha').annotate(Saldo=Sum('monto'))
    
    fig = px.line(
        x           = [c['fecha'] for c in mov],
        y           = [c['Saldo'] for c in mov],
        color       = [c['banco__name'] for c in mov],
        title       = "Resumen",
        markers     = True,
        labels      = {'x': 'Fecha', 'y': 'Monto'}
    )
    
    fig.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5
    })
    
    chart = fig.to_html()
    
    context = {'chart': chart}
    
    return render(request, 'chart.html', context)


def mov_banco_chart(empresa, banco_id):
    mov = MovimientoBancario.objects.filter(
        banco__empresa__random_short_uuid=empresa,banco_id=banco_id).values('banco','banco__name','fecha').order_by('banco','fecha').annotate(Saldo=Sum('monto'))
    
    fig = px.line(
        x       = [c['fecha'] for c in mov],
        y       = [c['Saldo'] for c in mov],
        color   = [c['banco__name'] for c in mov],
        title   = "Resumen",
        markers = True,
        labels  = {'x': 'Fecha', 'y': 'Monto'}
    )
    
    fig.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5
    })
    
    chart = fig.to_html()
    
    return chart


def comp_abono_cargo_chart(empresa, banco_id):
    mov = MovimientoBancario.objects.filter(banco__empresa__random_short_uuid=empresa,banco_id=banco_id).values('fecha', 'cargo_abono').order_by('fecha').annotate(Total=Sum('monto'))
    #print(mov)
    
    fig = px.bar(
        x       = [c['fecha'] for c in mov],
        y       = [c['Total'] for c in mov],
        color   = [c['cargo_abono'] for c in mov],
        title   = "Flujo: Abono vs Cargo",
        labels  = {'x': 'Fecha', 'y': 'Monto'},
        
    )
    
    fig.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5
    })
    
    abono_cargo_chart = fig.to_html()
    return abono_cargo_chart


def detalle_abonos_chart(empresa, banco_id):
    mov = MovimientoBancario.objects.filter(banco__empresa__random_short_uuid=empresa,banco_id=banco_id, cargo_abono="A").values('month_num', 'medio_de_pago__name').order_by('month_num').annotate(Ingresos=Sum('monto_positivo'))
    
    fig = px.bar(
        x = [c['month_num'] for c in mov],
        y = [c['Ingresos'] for c in mov],
        color = [c['medio_de_pago__name'] for c in mov],
        title = "Desglose Abonos x Mes",
        labels = {'x': 'Mes', 'y': 'Monto'},
    )
    
    fig.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5
    })
    
    detalle_abonos_chart = fig.to_html()
    return detalle_abonos_chart
    
    
# PRUEBA MODAL    
def get_modal(request):
    print("ENTERING MODAL")
    context = {}
    
    return render(request, 'test_modal.html', context)


#_____________________________________________________ END Plotly Charts _____________________________________________________#