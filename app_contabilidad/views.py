from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F, Sum, Count, Max, Q
import json
from datetime import datetime
import calendar
# Django Pivot
from django_pivot.pivot import pivot

# Tables
from django_tables2 import RequestConfig
from .tables import ComprobanteTable, LibroComprasTable, LibroVentasTable, ResumenEERRTable
# app_contabilidad
from .models import RegistroComprobante, Comprobante, LibroCompra, LibroVenta, CentroDeCostos, ClienteProveedor
from .forms import RegistroComprobanteForm, ComprobanteForm, LibroCompraForm, AgregarAuxiliarForm
# app_coa
from app_coa.models import COA
# app_empresa
from app_empresa.models import Empresa, DefaultCuentasContablesEmpresa
# app_banco
from app_banco.models import MovimientoBancario

# ___________________________________________________Contabilidad________________________________________________________________ #

@login_required
def get_info_contable(request, empresa):
    # Aqui vamos a tener la info general de la empresa
    # 
    # - Total de ventas por mes, compras por mes
    # - Estadisticas en general
    
    # - Se agrega temporalmente el <Reporte EERR>, luego se pasa a otra funcion o archivo
    if request.method == "GET":
        context = {'empresa': empresa}
        
        return render(request, 'contabilidad_info_empresa.html', context)
    
    
    if request.method == "POST":
        if request.POST.get('anio_select'):
            anio = int(request.POST.get('anio_select'))
        if request.POST.get('report_select') == "Estado de Resultado - Acumulado":
    
            data_empresa = Empresa.objects.get(random_short_uuid=empresa)
            
            compras_pendientes = LibroCompra.objects.filter(empresa__random_short_uuid=empresa, comprobante__es_done=False).count()
            ventas_pendientes = LibroVenta.objects.filter(empresa__random_short_uuid=empresa, comprobante__es_done=False).count()
            
            # Reporte EERR
            eerr_mensual_data = RegistroComprobante.objects.filter(Q(comprobante__empresa__random_short_uuid=empresa) & Q(comprobante__year_num=anio) &
                                                                (Q(cuenta_name__number__startswith='4') | Q(cuenta_name__number__startswith='5'))
                                                                    ).values('comprobante__month_num', 'cuenta_name__name')
            
            pivot_table = pivot(eerr_mensual_data, ['cuenta_name__number', 'cuenta_name__name'], 'comprobante__month_num', F('haber')-F('debe') ,default=0.0)

            #print(pivot_table)

            # Cambiando el Numero del mes por nombre (Se puede mejorar)
            for i in pivot_table:
                i['ENE'] = i.pop('1')
                i['FEB'] = i.pop('2')
                i['MAR'] = i.pop('3')
                i['ABR'] = i.pop('4')
                i['MAY'] = i.pop('5')
                i['JUN'] = i.pop('6')
                i['JUL'] = i.pop('7')
                i['AGO'] = i.pop('8')
                i['SEP'] = i.pop('9')
                i['OCT'] = i.pop('10')
                i['NOV'] = i.pop('11')
                try:
                    i['DIC'] = i.pop('12')
                except:
                    pass
            
            #test_table = ResumenEERRTable(data)
            test_table = ResumenEERRTable(pivot_table)
            
            
            context = {'data_empresa':data_empresa,
                    'empresa': empresa,
                    'compras_pendientes': compras_pendientes,
                    'ventas_pendientes': ventas_pendientes,
                    'eerr_mensual': pivot_table,
                    'test_table': test_table,
                    }
            
            return render(request, 'partials/contabilidad_informes/estado_de_resultado_acumulado.html', context)

@login_required
def get_libro_compras(request, empresa):
    
    """ 
        La idea es tener la informacion actual para trabajar mas eficiente.
        
        1) Filtrar por mes y anio actuales,
        Tambien poner otro filtro en el Front para que se pueda
        fechas anteriores.
    """
    
    # Date Variables
    today = datetime.today()
    mes = today.month
    anio = today.year    
    anio_options = [anio, anio-1, anio-2]
    mes_options = [1,2,3,4,5,6,7,8,9,10,11,12]
        
    # Data Empresa 
    data_empresa = Empresa.objects.get(random_short_uuid=empresa)
    # Data Libro Compras
    if request.GET.get('mes'):
        mes = int(request.GET.get('mes'))
        anio = int(request.GET.get('anio'))        
        # Filtra por mes y anio selecionados por el usuario
        libro_compras = LibroCompra.objects.filter(empresa__random_short_uuid=empresa, mes_contable = mes, ano_contable = anio)
    elif request.GET.get('pendientes') == 'True':
        # Mostrar todos los registros pendientes de clasificar
        libro_compras = LibroCompra.objects.filter(empresa__random_short_uuid=empresa, comprobante__es_done=False)
    elif request.GET.get('todos') == 'True':
        # Mostrar todos los registros >>>> MEJORAR por anio o algo mas eficiente
        libro_compras = LibroCompra.objects.filter(empresa__random_short_uuid=empresa)
    else:
        # Filtra por mes y anio actuales
        libro_compras = LibroCompra.objects.filter(empresa__random_short_uuid=empresa, mes_contable = mes, ano_contable = anio)

    #Table
    table = LibroComprasTable(libro_compras)
    
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=15)
    
    # Resumen Libro Compra x Tipo Documento
    resumen_compras = libro_compras.values('tipo_documento__nombre_documento').annotate(cantidad_dte = Count('tipo_documento'),
                                                                                        monto_exento = Sum('monto_exento'),
                                                                                        monto_neto = Sum('monto_neto'),
                                                                                        monto_iva = Sum('monto_iva'),
                                                                                        monto_total = Sum('monto_total'))
    
    # Totales Libro Compra
    total_compras = libro_compras.aggregate(cantidad_dte_total = Count('tipo_documento'),
                                            monto_exento_total = Sum('monto_exento'),
                                            monto_neto_total = Sum('monto_neto'),
                                            monto_iva_total = Sum('monto_iva'),
                                            monto_total_total = Sum('monto_total'))
    
    context = {'data_empresa':data_empresa,
               'table':table,
               'empresa': empresa,
               'mes': mes,
               'anio': anio,
               'anio_options': anio_options,
               'mes_options': mes_options,
               'resumen_compras': resumen_compras,
               'total_compras': total_compras,
               }
    
    return render(request, 'contabilidad_libro_compras_empresa.html', context)


@login_required
def get_detalle_compra(request, empresa, compra_pk):
    # Instance de la compra en revisión
    compra = LibroCompra.objects.get(pk=compra_pk)
    
    if request.method == "POST":
        form = LibroCompraForm(request.POST, instance=compra)
        if form.is_valid():
            form.save()
        else:
            print("FORM NOT VALIDO")
            print(form.errors)
        context = {
            'compra': compra,
            'compra_pk': compra_pk,
            'empresa': empresa,
        }

        return redirect(request.path)

    if request.method == "GET":
        # Valida si es Htmx Request
        is_htmx = request.headers.get('HX-Request')

        # Si es Htmx Request, se pide editar registro.
        if is_htmx:
            
            compra_form = LibroCompraForm(instance=compra)
            context = {
                'compra': compra,
                'compra_pk': compra_pk,
                'empresa': empresa,
                'compra_form': compra_form,
            }
            
            return render(request, 'partials/libro_compras_detalle_form.html', context)
        
        # Filtrando las cuentas "Leaf" que se puede utilizar
        coa = COA.objects.filter(rght=F('lft')+1)
        context = {
                'compra': compra,
                'compra_pk': compra_pk,
                'empresa': empresa,
                'coa': coa,
            }
        return render(request, 'libro_compras_detalle.html', context)



@login_required
def get_libro_ventas(request, empresa):
    
    """ 
        La idea es tener la informacion actual para trabajar mas eficiente.
        
        1) Filtrar por mes y anio actuales,
        Tambien poner otro filtro en el Front para que se pueda
        fechas anteriores.
    """
    
    # Date Variables
    today = datetime.today()
    mes = today.month
    anio = today.year    
    anio_options = [anio, anio-1, anio-2]
    mes_options = [1,2,3,4,5,6,7,8,9,10,11,12]
        
    # Data Empresa
    data_empresa = Empresa.objects.get(random_short_uuid=empresa)
    compras_pendientes = LibroCompra.objects.filter(empresa__random_short_uuid=empresa, comprobante__es_done=False).count()
    ventas_pendientes = LibroVenta.objects.filter(empresa__random_short_uuid=empresa, comprobante__es_done=False).count()
    
    # Data Libro Ventas
    if request.GET.get('mes'):
        mes = int(request.GET.get('mes'))
        anio = int(request.GET.get('anio'))        
        # Filtra por mes y anio selecionados por el usuario
        libro_ventas = LibroVenta.objects.filter(empresa__random_short_uuid=empresa, mes_contable = mes, ano_contable = anio)
    elif request.GET.get('pendientes') == 'True':
        # Mostrar todos los registros pendientes de clasificar
        libro_ventas = LibroVenta.objects.filter(empresa__random_short_uuid=empresa, comprobante__es_done=False)
    elif request.GET.get('todos') == 'True':
        # Mostrar todos los registros >>>> MEJORAR por anio o algo mas eficiente
        libro_ventas = LibroVenta.objects.filter(empresa__random_short_uuid=empresa)
    else:
        # Filtra por mes y anio actuales
        libro_ventas = LibroVenta.objects.filter(empresa__random_short_uuid=empresa, mes_contable = mes, ano_contable = anio)
    
    #Table
    table = LibroVentasTable(libro_ventas)
    
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=15)
    
    # Resumen Libro Venta x Tipo Documento
    resumen_ventas = libro_ventas.values('tipo_documento__nombre_documento').annotate(cantidad_dte = Count('tipo_documento'),
                                                                                        monto_exento = Sum('monto_exento'),
                                                                                        monto_neto = Sum('monto_neto'),
                                                                                        monto_iva = Sum('monto_iva'),
                                                                                        monto_total = Sum('monto_total'))
    
    # Totales Libro Venta
    total_ventas = libro_ventas.aggregate(cantidad_dte_total = Count('tipo_documento'),
                                            monto_exento_total = Sum('monto_exento'),
                                            monto_neto_total = Sum('monto_neto'),
                                            monto_iva_total = Sum('monto_iva'),
                                            monto_total_total = Sum('monto_total'))
    
    context = {'data_empresa':data_empresa,
               'table':table,
               'empresa': empresa,
               'mes': mes,
               'anio': anio,
               'anio_options': anio_options,
               'mes_options': mes_options,
               'resumen_ventas': resumen_ventas,
               'total_ventas': total_ventas,
               'compras_pendientes': compras_pendientes,
               'ventas_pendientes': ventas_pendientes,
               }
    
    return render(request, 'contabilidad_libro_ventas_empresa.html', context)


@login_required
def magic_libro_ventas(request, empresa):
    
    """ 
    Primer test: funciona, pero es MUY poco eficiente
    Se puede hacer loop donde se clasifica cada uno (ver si bulk_create es bueno, no dispara el metodo save() en los modelos)
    Ver si se puede hacer un Ajuste General por <Empresa> asi se lleva las cuentas contables definidas previamente
    """
    empresa_actual = Empresa.objects.get(random_short_uuid=empresa)
    def_cuantas_contables = empresa_actual.def_cuentas_contables
    ventas_pendientes = LibroVenta.objects.filter(empresa__random_short_uuid=empresa, comprobante__es_done=False, tipo_documento__cod_documento=39)
    
    
    cantidad_ventas_pendientes = ventas_pendientes.count()
    
    # COA - por ahora manuales para las pruebas
    boletas_de_ventas = def_cuantas_contables.default_ventas
    iva_debito = def_cuantas_contables.default_iva_ventas
    ventas_con_boletas = COA.objects.get(id=165)
    centro_costo = CentroDeCostos.objects.get(id=7)
    
    
    
    for i in range(cantidad_ventas_pendientes):
        if ventas_pendientes[0].tipo_documento.cod_documento == "39":    
            comprobante = ventas_pendientes[0].comprobante
            
            RegistroComprobante.objects.bulk_create([
                RegistroComprobante(comprobante=comprobante, cuenta_name=boletas_de_ventas, debe=ventas_pendientes[0].monto_total, haber=0, cliente_proveedor = ventas_pendientes[0].proveedor, numero_documento= ventas_pendientes[0].folio),
                RegistroComprobante(comprobante=comprobante, cuenta_name=iva_debito, debe=0, haber=ventas_pendientes[0].monto_iva),
                RegistroComprobante(comprobante=comprobante, cuenta_name=ventas_con_boletas, centro_costo=centro_costo, debe=0, haber=ventas_pendientes[0].monto_neto),

            ])
        
            print(comprobante)
            comprobante.es_done = True
            comprobante.save()
    
    return redirect(reverse('get-libro-ventas', kwargs={'empresa':empresa}) + f"?mes=5&anio=2023") #Hacer que haga Refresh la hoja
    
    
    


# ___________________________________________________End Contabilidad____________________________________________________________ #

# ___________________________________________________Comprobantes________________________________________________________________ #
   
    
@login_required    
def comprobante_list(request, empresa):
    
    data_empresa = Empresa.objects.get(random_short_uuid=empresa)
    
    if request.method == "GET":
        # Filtra por Pendientes
        if request.GET.get("es_done"):
            es_done = request.GET.get("es_done")
            table = ComprobanteTable(Comprobante.objects.filter(empresa__random_short_uuid=empresa, es_done=es_done))
        # Sin filtro Pendientes
        else:
            table = ComprobanteTable(Comprobante.objects.filter(empresa__random_short_uuid=empresa))

    # Comprobante Table
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=20)
    
    context = {'table': table, 'data_empresa':data_empresa, 'empresa': empresa}
    
    return render(request, 'table.html', context)


@login_required
def add_comprobante(request, empresa):
    
    if request.method == "GET":    
        
        context = {
            'comprobante_form': ComprobanteForm(initial={'numero_comprobante':0}), # Ver si crear otro Form para no tener conflictos con views.contabilizar_comprobante()
            'empresa': empresa,
            }
            
        return render(request, 'add_comprobante.html', context)
    
    if request.method == "POST":
        tipo = request.POST.get('tipo')
        fecha = datetime.strptime(request.POST.get('fecha'), '%Y-%m-%d')
        glosa = request.POST.get('glosa')
        empresa = Empresa.objects.get(random_short_uuid=empresa)
        
        last_num = Comprobante.objects.filter(empresa=empresa ,tipo=tipo, numero_comprobante__gte=5999999, numero_comprobante__lte=7000000).aggregate(Max('numero_comprobante'))

        if last_num['numero_comprobante__max'] == None:
            comprobante_num = 6000000
        else:
            comprobante_num = last_num['numero_comprobante__max'] + 1

        comprobante = Comprobante.objects.create(
            numero_comprobante = comprobante_num,
            fecha = fecha,
            tipo = tipo,
            empresa = empresa,
            glosa = glosa
            )
        return redirect(reverse('contabilizar-comprobante', kwargs={'empresa':empresa.random_short_uuid, 'pk':comprobante.id}))




@login_required
def contabilizar_comprobante(request, empresa, pk):
        
    if request.method == 'GET':
        
        # Se manda Info de COA como JSON.
        empresa_actual = Empresa.objects.get(random_short_uuid=empresa)
        
        coa = list(COA.objects.filter(coa_name=empresa_actual.plan_de_cuentas ,rght=F('lft')+1).values_list('pk', 'number', 'name', 'es_banco', 'es_auxiliar', 'es_centro_de_costos', 'es_sucursal', 'es_honorarios' ).order_by('number'))
        my_dict = [dict(zip(('id','number', 'name', 'es_banco', 'es_auxiliar', 'es_centro_de_costos', 'es_sucursal', 'es_honorarios'), x)) for x in coa]
        
        # El numero del <comprobante> que trabajamos (contabilizamos en este caso)
        comprobante = Comprobante.objects.get(id=pk)
        n_comprobante = comprobante.numero_comprobante
        
        # Si el comprobante NO se encuentra Contabilizado, sigue a contabilizar
        if comprobante.es_done == False:        
            # PENDIENTE - segun tipo comprobante se agrega info ayuda
            
            # Compra
            if str(n_comprobante)[0] == "3":
                try:
                    compra = LibroCompra.objects.get(comprobante__id=pk)            
                    datos_mov = f"{compra.proveedor} | Monto -> Exento: {compra.monto_exento} | Neto: {compra.monto_neto} | Iva: {compra.monto_iva} | Total:{compra.monto_total} "
                    datos_mov2 = [f"Proveedor: {compra.proveedor} | Folio: {compra.folio}",f"Exento: {compra.monto_exento}",f"Neto: {compra.monto_neto}",f"Iva: {compra.monto_iva}",f"Total: {compra.monto_total}"]
                except:
                    datos_mov = "No Info"
                    datos_mov2 = "No Info"
                print("SI es compras")
            # Venta
            elif str(n_comprobante)[0] == "4":
                try:
                    #MEJORAR
                    venta = LibroVenta.objects.get(comprobante__id=pk)
                    #print(LibroVenta.objects.get(comprobante__id=pk))
                    datos_mov = f"{venta.proveedor} | Monto -> Exento: {venta.monto_exento} | Neto: {venta.monto_neto} | Iva: {venta.monto_iva} | Total:{venta.monto_total} "
                    datos_mov2 = [f"Proveedor: {venta.proveedor} | Folio: {venta.folio}",f"Exento: {venta.monto_exento}",f"Neto: {venta.monto_neto}",f"Iva: {venta.monto_iva}",f"Total: {venta.monto_total}"]
                except:
                    datos_mov = "No Info"
                    datos_mov2 = ["NO INFO",]
                print("SI es ventas")
            # Banco
            elif str(n_comprobante)[0] == "1":
                try:
                    mov_banco = MovimientoBancario.objects.get(comprobante__id=pk)
                    datos_mov = f"Tipo: Movimiento Bancario >> Monto: {mov_banco.monto}"
                    datos_mov2 = [f"Movimiento Bancario >> Monto: {mov_banco.monto}",]
                except:
                    datos_mov = "No Info"
                    datos_mov2 = "No Info"
                print("SI es banco")
            # Otro
            else:
                datos_mov = ""
                datos_mov2 = ["NO INFO",]
                
            context = {'registro_form': RegistroComprobanteForm(initial={'comprobante': comprobante,},), #empresa=empresa_actual.country
                    'pk_comp':pk,
                    'obj': json.dumps(my_dict),
                    'comprobante': comprobante,
                    'comprobante_form':ComprobanteForm(instance=comprobante),
                    'empresa': empresa ,
                    'datos_mov': datos_mov,
                    'datos_mov2': datos_mov2,          
                    }
                
            return render(request, 'contabilizar_comprobante.html', context)
        
        # Si el comprobante se encuentra Contabilizado, hace redirect
        else:
            
            registro_comprobante = RegistroComprobante.objects.filter(comprobante=comprobante)
            
            context = {
                'empresa': empresa,
                'pk_comp':pk,
                'comprobante': comprobante,
                'registro_comprobante': registro_comprobante,
            }
            return render(request, 'detalle_comprobante_contabilizado.html', context)
    
    if request.method == 'POST':
        comprobante = Comprobante.objects.get(id=pk)
        print('entrando POST')
        #print(request.POST)
        # Form Fields
        indexes = list(request.POST)
        # Convert to Dict
        forms = dict(request.POST)
        num_forms = len(forms['cuenta_name'])
        
        result = validar_forms_reglas_contables(forms, num_forms, comprobante) #PENDIENTE
        print(result['sum_debe'])
        # Loop cada Form, populando su fields y Save()
        for f in range(num_forms):
            form2 = {}
            for i in range(len(indexes)):
                form2[indexes[i]] = forms[indexes[i]][f]
            if form2['debe'] == '0' and form2['haber'] == '0':
                pass
            else:
                form = RegistroComprobanteForm(form2 or None)
                if form.is_valid():
                    print("VALIDO")
                    form.save()
                else:
                    print("FORM INVALIDO")
        # Marcar Comprobante como terminado (es_done)
        comprobante.es_done = True
        comprobante.suma_debe = result['sum_debe']
        comprobante.suma_haber = result['sum_haber']
        comprobante.save()

        registro_comprobante = RegistroComprobante.objects.filter(comprobante=comprobante)
        context = {
                'empresa': empresa,
                'pk_comp':pk,
                'comprobante': comprobante,
                'registro_comprobante': registro_comprobante,
            }
        response = HttpResponse()
        response['HX-Refresh'] = "true"
        
        return response


@login_required
def add_registro(request, empresa, pk):
    print("ENTERING FORM 2")
    coa = COA.objects.filter(rght=F('lft')+1)
    comprobante = Comprobante.objects.get(id=pk)

    context = {'registro_form': RegistroComprobanteForm(initial={'comprobante': comprobante, }),
               'coa': coa,
               'comprobante_form':ComprobanteForm(instance=comprobante)}
    
    return render(request, 'partials/registro_comprobante_form.html', context)


@login_required
def get_info_cuenta_contable(request, empresa):
    print("ENTERING COA")
    var = request.GET.get('cuenta_name')

    coa = list(COA.objects.filter(rght=F('lft')+1).values_list('pk', 'number', 'name', 'es_banco', 'es_auxiliar', 'es_centro_de_costos', 'es_sucursal', 'es_honorarios' ).order_by('number'))
    my_dict = [dict(zip(('id','number', 'name', 'es_banco', 'es_auxiliar', 'es_centro_de_costos', 'es_sucursal', 'es_honorarios'), x)) for x in coa]
    
    context = {}#'obj': json.dumps(my_dict)}
    ## Falta agregar Headers para que CC y Sucursal los escuchan (2 headers en este caso)
    ## Eliminar el attr <disabled> en caso si la cuenta lo requiere
    
    
    
    return render(request, 'partials/get_coa.html', context)



def add_auxiliar(request, empresa):
    
    result_message = {}
    add_aux_form = AgregarAuxiliarForm()
    
    if request.method == "POST":
        """
            Se creal un <ClienteProveedor> en caso que no existe.
            Primero revisa y luego lo crea si el <rut> esta disponible.
            
            El usuario debe agregar nuevo <RegistroComprobanteForm> para ver el nuevo <ClienteProveedor>
            
            Nota: SE PUEDE MEJORAR
        """
        rut = request.POST.get('rut')
        razon_social = request.POST.get('razon_social')
        status = request.POST.get('es_agregar')
        if ClienteProveedor.objects.filter(rut=rut).exists() and status == "False":
            aux = ClienteProveedor.objects.filter(rut=rut).first()
            result_message['razon_social'] = aux.razon_social
            result_message['message_failure'] = "Rut Existe:"
            result_message['rut'] = rut
            result_message['status'] = "False"
        elif status == "True":
            print("CREANDO")
            ClienteProveedor.objects.create(rut=rut,razon_social=razon_social)
            result_message['message_success'] = "Auxiliar Creado con Éxito!"
        else:
            result_message['message_success'] = "Rut Disponible!"
            result_message['rut'] = rut
            result_message['status'] = "True" 
            add_aux_form = AgregarAuxiliarForm(initial={'rut': rut, 'razon_social': razon_social})
    
    context = {'empresa': empresa,
               'add_aux_form': add_aux_form,
               'result_message': result_message}

    return render(request, 'partials/add_auxiliar_modal.html', context)




# ___________________________________________________End Comprobantes________________________________________________________________ #


# ___________________________________________________ Impuestos     ________________________________________________________________ #


def get_index_tax(request, empresa):
    if request.method == "POST":
        mes = int(request.POST.get('tax_mes_select'))
        anio = int(request.POST.get('tax_anio_select'))
    else:
        mes = datetime.today().month
        anio = datetime.today().year
    empresa_analisis = Empresa.objects.get(random_short_uuid=empresa)
    
    #print(empresa_analisis.def_cuentas_contables.default_iva_ventas)
    
    iva_debito = empresa_analisis.def_cuentas_contables.default_iva_ventas_id
    iva_credito = empresa_analisis.def_cuentas_contables.default_iva_compras_id
    
    total_debito = RegistroComprobante.objects.filter(comprobante__empresa=empresa_analisis,
                                           cuenta_name_id=iva_debito,
                                           comprobante__month_num=mes,
                                           comprobante__year_num=anio,
                                           ).aggregate(total_debito=Sum(F('haber')-F('debe'), default=float(0)))
    
    total_credito = RegistroComprobante.objects.filter(comprobante__empresa=empresa_analisis,
                                           cuenta_name_id=iva_credito,
                                           comprobante__month_num=mes,
                                           comprobante__year_num=anio,
                                           ).aggregate(total_credito=Sum(F('debe')-F('haber'), default=float(0)))
    try:
        por_pagar = total_debito.get('total_debito') - total_credito.get('total_credito')
        if por_pagar < 0:
            por_pagar = 0
    except:
        por_pagar = 'Err'
    
    context = {
        'empresa': empresa,
        'total_debito': total_debito.get('total_debito'),
        'total_credito': total_credito.get('total_credito'),
        'por_pagar': por_pagar,
    }


    return render(request, "tax/tax_index.html", context)




# ___________________________________________________ End Impuestos ________________________________________________________________ #


# ___________________________________________________Form Helper_____________________________________________________________________ #


# Aqui validamos que la data que nos llega de los Forms como POST al <views.contabilizar_comprobante>
#
# Criterios:
# 1) Suma Debe y Haber DEBEN cuadrar!
# 2) <Comprobante Original> es igual a los <Registros>
# 3)
# 4)

def validar_forms_reglas_contables(forms, num_forms, comprobante):
    result = {}
    sum_debe = 0
    sum_haber = 0
    # Comprobante
    comprobante_original = comprobante.pk
    # Valor inicial True, luego basta uno que no es igual para levantar error.
    comprobante_test_result = True
    
    
    for x in range(num_forms):
        # Suma Total >> Debe y Haber
        sum_debe += int(forms['debe'][x])
        sum_haber += int(forms['haber'][x])
        # Comparamos N°Comprobante Original es igual a los registros.
        if int(forms['comprobante'][x]) != comprobante_original:
            comprobante_test_result = False
    
    if sum_debe != sum_haber:
        result['dif_sum'] = sum_debe - sum_haber
    
    result['comprobante_test_result'] = comprobante_test_result
    result['sum_debe'] = sum_debe
    result['sum_haber'] = sum_haber
        
    #print(result)
    return result


    
    




# ___________________________________________________End Form Helper_________________________________________________________________ #
