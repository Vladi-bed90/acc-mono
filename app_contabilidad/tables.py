import django_tables2 as tables
from django_tables2.utils import Accessor
from .models import Comprobante, LibroCompra, LibroVenta


# Format Float to display like Integer
# https://stackoverflow.com/questions/48546729/how-to-format-the-display-of-floats-when-using-django-tables2
class NumberColumn(tables.Column):
    def render(self, value):
        # https://www.w3schools.com/python/ref_string_format.asp    
        return '$ {:,.0f}'.format(value)


class ComprobanteTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    # Agregar Acciones
    acciones = tables.TemplateColumn(template_code="<a href={% url 'contabilizar-comprobante' empresa record.pk %} id='{{record.id}}' {% if record.es_done %} class='btn btn-sm btn-success disabled' {% else %} class='btn btn-sm btn-success' {% endif %} >Contabilizar</a>",
                                     attrs={
                                         '_': lambda record: 'if {{record.es_done}} set .disabled to me'
                                     })
    
    class Meta:        
        model = Comprobante
        row_attrs = {
            "value": lambda record: record.pk,            
        }  
        sequence = ('selection', )
        exclude = ( 'id_unico', 'day_num', 'month_num', 'year_num', 'empresa', 'es_cuadrado')
        
    # Modificar Attrs de la tabla
    # record – the entire record for the row from the table data
    # value – the value for the cell retrieved from the table data    
    es_done = tables.BooleanColumn(attrs={
        "td": {
            'class': lambda record: "text-success fw-bold" if record.es_done else "text-danger fw-bold"
        }
    })
    fecha = tables.DateColumn(format='d/m/Y')
    suma_debe = NumberColumn()
    suma_haber = NumberColumn()
    
    
    
class LibroComprasTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    periodo_contable = tables.TemplateColumn(verbose_name="Periodo", 
                                             template_code="<p class='text-center'>{{record.mes_contable}}-{{record.ano_contable}}</p>",
                                             )
    # Agregar Acciones
    acciones = tables.TemplateColumn(template_name='partials/libro_compras/acciones.html')
        
    comp_done = tables.BooleanColumn(accessor=Accessor("comprobante.es_done"), verbose_name="*Done")
    class Meta:
        model = LibroCompra
        row_attrs = {
            "value": lambda record: record.pk,
            "class": "align-middle",
        }
        sequence = ('selection', 'id', 'tipo_documento', 'folio', 'fecha_documento', 'proveedor', 'monto_exento', 'monto_neto', 'monto_iva', 'monto_total', 'detalle', 'comp_done')
        exclude = ('id', 'empresa', 'id_unico_dte', 'mes_contable', 'ano_contable', 'rut_registro', 'es_cuadrado', 'monto_contabilizado', 'es_pagado', 'monto_positivo','comprobante', 'es_done', 'es_anulado')
    
    folio = tables.TemplateColumn(template_code="<p class='text-center fw-bold' title='{{record.folio}}'>{{record.folio}}</p>")
        
    fecha_documento = tables.DateColumn(format='d/m/Y', attrs={
        "td": {
            "class": "text-center",
        }
    })
    tipo_documento = tables.TemplateColumn(template_code="<p title='{{record.tipo_documento}}' class='text-center {% if record.monto_total < 0 %} bg-danger {% endif %} '>{{record.tipo_documento|truncatechars:20}}</p>")
    proveedor = tables.TemplateColumn(template_code="<p class='fw-bold' title='{{record.proveedor}}'>{{record.proveedor|truncatechars:30}}</p>")
    monto_exento = NumberColumn(verbose_name="Exento", attrs= {
        "td": {
            "align": "right",
        }
    })
    monto_neto = NumberColumn(verbose_name="Neto", attrs= {
        "td": {
            "class": "",
            "align": "right",
        }
    })
    monto_iva = NumberColumn(verbose_name="IVA", attrs= {
        "td": {
            "class": "",
            "align": "right",
        }
    })
    monto_total = NumberColumn(verbose_name="Bruto", attrs= {
        "td": {
            "align": "right",
            "class": "fw-bold",
        }
    })
    comprobante = tables.TemplateColumn(template_code="<p class='text-center'>{{record.comprobante}}</p>")
    detalle = tables.TemplateColumn(template_code="<p title='{{record.detalle}}' class='text-center'>{% if record.detalle %}{{record.detalle|truncatechars:15}}{% else %}---{% endif %}</p>")
    
    


class LibroVentasTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    periodo_contable = tables.TemplateColumn(verbose_name="Periodo", 
                                             template_code="<p class='text-center'>{{record.mes_contable}}-{{record.ano_contable}}</p>",
                                             )
    # Agregar Acciones
    acciones = tables.TemplateColumn(
        template_code="<div class='btn-group'><a href='#' id='{{record.id}}' class='btn btn-sm btn-success'>Ver</a>"
        "<a href='{% url 'contabilizar-comprobante' data_empresa.random_short_uuid record.comprobante_id %}' id='{{record.comprobante_id}}' class='btn btn-sm btn-warning'>Clas</a>"
        "<a href='#' id='{{record.comprobante_id}}' class='btn btn-sm btn-light'>R</a></div>")
    comp_done = tables.BooleanColumn(accessor=Accessor("comprobante.es_done"), verbose_name="*Done")
    class Meta:
        model = LibroVenta
        row_attrs = {
            "value": lambda record: record.pk,           
        }
        sequence = ('selection', 'id', 'tipo_documento', 'folio', 'fecha_documento', 'proveedor', 'monto_exento', 'monto_neto', 'monto_iva', 'monto_total', 'detalle', 'comp_done')
        exclude = ('id', 'empresa', 'id_unico_dte', 'mes_contable', 'ano_contable', 'rut_registro', 'es_cuadrado', 'monto_contabilizado', 'es_pagado', 'monto_positivo','comprobante', 'es_done')
    
    folio = tables.TemplateColumn(template_code="<p class='text-center fw-bold' title='{{record.folio}}'>{{record.folio}}</p>")
        
    fecha_documento = tables.DateColumn(format='d/m/Y', attrs={
        "td": {
            "class": "text-center",
        }
    })
    tipo_documento = tables.TemplateColumn(template_code="<p title='{{record.tipo_documento}}'>{{record.tipo_documento|truncatechars:20}}</p>")
    proveedor = tables.TemplateColumn(template_code="<p class='fw-bold' title='{{record.proveedor}}'>{{record.proveedor|truncatechars:30}}</p>")
    monto_exento = NumberColumn(verbose_name="Exento", attrs= {
        "td": {
            "align": "right",
        }
    })
    monto_neto = NumberColumn(verbose_name="Neto", attrs= {
        "td": {
            "class": "fs-6",
            "align": "right",
        }
    })
    monto_iva = NumberColumn(verbose_name="IVA", attrs= {
        "td": {
            "class": "fs-6",
            "align": "right",
        }
    })
    monto_total = NumberColumn(verbose_name="Bruto", attrs= {
        "td": {
            "align": "right",
            "class": "fs-6 fw-bold",
        }
    })
    comprobante = tables.TemplateColumn(template_code="<p class='text-center'>{{record.comprobante}}</p>")
    detalle = tables.TemplateColumn(template_code="<p title='{{record.detalle}}' class='text-center'>{% if record.detalle %}{{record.detalle|truncatechars:15}}{% else %}---{% endif %}</p>")
    


# Resumen EERR Table
class ResumenEERRTable(tables.Table):
    
    th_attrs = {"th": {"class": "text-start"}}
    
    cuenta_name__number = tables.Column(verbose_name="# Cuenta")
    cuenta_name__name = tables.Column(verbose_name="Nombre Cuenta")
    ENE = tables.TemplateColumn(template_code="{% if record.ENE >= 0.0 %} <span>$ {{record.ENE|floatformat:'g'}}</span> {% else %} <span class='text-danger'>($ {{record.ENE|floatformat:'g'}})</span> {% endif %}", attrs=th_attrs)
    FEB = tables.TemplateColumn(template_code="$ {{record.FEB|floatformat:'g'}}")
    MAR = tables.TemplateColumn(template_code="$ {{record.MAR|floatformat:'g'}}")
    ABR = tables.TemplateColumn(template_code="$ {{record.ABR|floatformat:'g'}}")
    MAY = tables.TemplateColumn(template_code="$ {{record.MAY|floatformat:'g'}}")
    JUN = tables.TemplateColumn(template_code="$ {{record.JUN|floatformat:'g'}}")
    JUL = tables.TemplateColumn(template_code="$ {{record.JUL|floatformat:'g'}}")
    AGO = tables.TemplateColumn(template_code="$ {{record.AGO|floatformat:'g'}}")
    SEP = tables.TemplateColumn(template_code="$ {{record.SEP|floatformat:'g'}}")
    OCT = tables.TemplateColumn(template_code="$ {{record.OCT|floatformat:'g'}}")
    NOV = tables.TemplateColumn(template_code="$ {{record.NOV|floatformat:'g'}}")
    DIC = tables.TemplateColumn(template_code="$ {{record.DIC|floatformat:'g'}}")
    
    
    