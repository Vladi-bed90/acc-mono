from django.shortcuts import render
from .models import UploadCartolaBanco, UploadComprasChile, UploadVentasChile
from .forms import UploadCartolaBancoForm, UploadComprasChileForm, UploadVentasChileForm
# Banco
from app_banco.models import MovimientoBancario
# Contabilidad
from app_contabilidad.models import LibroCompra, LibroVenta, ClienteProveedor, TipoDocumentoTributario
# Empresa
from app_empresa.models import Empresa

import csv
import datetime


def upload_index(request):
    cartola_banco_form = UploadCartolaBancoForm()
    cartola_compras_form = UploadComprasChileForm()
    
    context = {'cartola_banco_form':cartola_banco_form, 'cartola_compras_form':cartola_compras_form}
    return render(request, 'upload_files_index.html', context)


# Cartola Generica
# Nota --> Django automaticamente agrega _id a FK Keys, por lo tanto hay que ver bien los PK en el Loop
def upload_cartola_generica(request):
    form = UploadCartolaBancoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = UploadCartolaBancoForm()
        obj = UploadCartolaBanco.objects.get(activated=False)
        with open(obj.file_name.path, "r") as f:
            reader = csv.reader(f)
            
            for i, row in enumerate(reader):
                if i == 0:
                    pass
                else:
                    row = "".join(row)
                    row = row.split(";")
                    MovimientoBancario.objects.create(
                        fecha = datetime.datetime.strptime(row[0], "%d/%m/%Y"),
                        monto = int(row[1]),
                        descripcion = row[2],
                        cargo_abono = row[3],
                        detalle_adicional = row[4],
                        banco_id = row[5],
                    )
            obj.activated = True
            obj.save()
    return render(request, "partials/upload_cartola_banco.html", {"form": form})


# Libro Compra Chile
def upload_libro_compras_chile(request):
    form = UploadComprasChileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        print("FORM VALID")
        form.save()
        form = UploadComprasChileForm()
        obj = UploadComprasChile.objects.get(activated=False)
        with open(obj.file_name.path, "r") as f:
            reader = csv.reader(f)
            
            for i, row in enumerate(reader):
                if i == 0:
                    pass
                else:
                    row = "".join(row)
                    row = row.split("\t")
                    if ClienteProveedor.objects.filter(rut = row[3]).exists():
                        proveedor_nuevo = ClienteProveedor.objects.get(rut = row[3])
                    else:
                        proveedor_nuevo = ClienteProveedor.objects.create(rut = row[3], razon_social = row[4], pais_id = 1) # Cambiar pais = 1 a mas dinamico
                        
                    LibroCompra.objects.create(
                        tipo_documento = TipoDocumentoTributario.objects.get(cod_documento = row[0]),
                        folio = row[1],
                        fecha_documento = datetime.date(int(row[10]), int(row[9]), 1),
                        proveedor = proveedor_nuevo,
                        monto_exento = float(row[5]),
                        monto_neto = float(row[6]),
                        monto_iva = float(row[7]),
                        monto_total = float(row[8]),
                        mes_contable = row[9],
                        ano_contable = row[10],
                        empresa_id = row[11]
                        
                    )
            obj.activated = True
            obj.save()
    return render(request, 'partials/upload_libro_compras_chile.html', {'form':form} )


# Libro Ventas Chile
def upload_libro_ventas_chile(request):
    form = UploadVentasChileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = UploadVentasChileForm()
        obj = UploadVentasChile.objects.get(activated=False)
        with open(obj.file_name.path, "r") as f:
            reader = csv.reader(f)
            
            for i, row in enumerate(reader):
                # Skip headers
                if i == 0:
                    pass
                else:
                    row = "".join(row)
                    row = row.split(";")
                    
                    rut = row[3].replace(".","")
                    # Revisa si existe el Proveedor/Cliente. Sino, lo crea.
                    if ClienteProveedor.objects.filter(rut = rut).exists():
                        proveedor_nuevo = ClienteProveedor.objects.get(rut = rut)
                    else:
                        proveedor_nuevo = ClienteProveedor.objects.create(rut = rut, razon_social = row[4], pais_id = 1) # Cambiar pais = 1 a mas dinamico
                    
                    # Revisando si ya existe el DTE
                    id_unico_row = f"{rut}.{row[0]}.{row[1]}"
                    if LibroVenta.objects.filter(id_unico_dte = id_unico_row).exists():
                        pass
                    else:    
                        LibroVenta.objects.create(
                            tipo_documento = TipoDocumentoTributario.objects.get(cod_documento = row[0]),
                            folio = row[1],
                            fecha_documento = datetime.datetime.strptime(row[2], "%d-%m-%Y"),
                            proveedor = proveedor_nuevo,
                            monto_exento = float(row[5]),
                            monto_neto = float(row[6]),
                            monto_iva = float(row[7]),
                            monto_total = float(row[8]),
                            mes_contable = row[9],
                            ano_contable = row[10],
                            empresa_id = row[11]                        
                        )
            # Activando el archivo
            obj.activated = True
            obj.save()
    return render(request, 'partials/upload_libro_ventas_chile.html', {'form':form} )