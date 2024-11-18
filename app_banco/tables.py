from django.contrib.humanize.templatetags.humanize import intcomma
import django_tables2 as tables
from django_tables2.utils import Accessor
from .models import MovimientoBancario


class MovimientoBancarioTable(tables.Table):
    # Extra Fields
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    # IGNORAR POR AHORA >> comp_id = tables.Column(accessor='comprobante.id', verbose_name='Ver')
    
    # https://docs.djangoproject.com/en/4.2/ref/templates/builtins/ -->> Se utiliza Tag {% widthratio %}
    # Casos Ejemplo -->> https://stackoverflow.com/questions/8447913/is-there-a-filter-for-divide-for-django-template
    Progreso = tables.TemplateColumn(
        template_code='<div class="progress" style="height: 10px;"><div class="progress-bar" role="progressbar" style="width: {% widthratio record.monto_contabilizado record.monto_positivo 100 %}%" aria-valuenow="1" aria-valuemin="0" aria-valuemax="100"></div></div>',
        attrs = {
            "align": "center",
            "text": "center"
        }
        )
    # Accion Buttons
    acciones = tables.TemplateColumn(
        template_code="<a href='{% url 'get-mov-detalle' empresa data_banco.id record.id %}' id='{{record.id}}' class='btn btn-sm btn-info py-1'>Ver</a>", attrs={
        "td": {
            'class': 'text-center',
        }
    }) 
    comp_done = tables.BooleanColumn(accessor=Accessor("comprobante.es_done"), verbose_name="*Done", attrs={
        "td": {
            'style': lambda record: 'color:green; font-size: 20px; text-align: center;' if record.comprobante.es_done else 'color:red; font-size: 20px; text-align: center;',
        }
    })
    class Meta:
        model = MovimientoBancario
        # Attr de las filas
        row_attrs = {
            "value": lambda record: record.pk,
            "class": "align-middle font-monospace",
            "style": '',
        } 
        exclude = ('id','uploaded_by', 'created_at', 'monto_positivo', 'day_num', 'month_num', 'year_num', 'banco', 'monto_contabilizado', 'rut_chile', 'esta_contabilizado')
        sequence = ('selection', 'monto', 'fecha','descripcion','cargo_abono', 'detalle_adicional', 'medio_de_pago', 'comprobante', 'comp_done' )
    
    
    # Modificar Attrs de la tabla
    # record – the entire record for the row from the table data
    # value – the value for the cell retrieved from the table data 
       
    cargo_abono = tables.Column(verbose_name= 'Tipo' ,attrs={
        "td": {
            'class': lambda record: "text-success fw-bold" if record.cargo_abono == "A" else "text-danger fw-bold",
            "align": "center"
        }
    })
    # Agregar Modal para editar Medio_de_pago
    medio_de_pago = tables.TemplateColumn(
        attrs={
            "td": {
                'contenteditable': 'false',
                'id': lambda record: 'mp_' + str(record.pk)        
            }},
        template_code="<span>{% if record.cargo_abono == 'A' %}<a class='btn btn-sm btn-warning' hx-get='{% url 'modificar-medio-de-pago' empresa data_banco.id record.id %}' hx-trigger='click' hx-target='#mp_{{record.id}}' ><i class='fa-regular fa-pen-to-square'></i></a>{% endif %} {{record.medio_de_pago}}</span>"   
        )
    
    esta_contabilizado = tables.BooleanColumn(verbose_name='OK' ,attrs={
        "td": {
            'class': lambda record: "text-success fw-bold" if record.esta_contabilizado else "text-danger fw-bold",
            "align": "center"
        }
    })
    
    monto = tables.TemplateColumn(
        attrs = {"td":{
            'class': lambda record: "text-success fw-bold" if record.cargo_abono == "A" else "text-danger fw-bold",
            "align": "right"
            }},
        template_code="<span>${{record.monto|floatformat:'g'}} </span>",
        )
    fecha = tables.DateColumn(format='d/m/Y', attrs={
        "td": {
            'class': "text-center",
            "align": "center"
        }
    })
    comprobante = tables.TemplateColumn(
        template_code="<a class='badge rounded-pill text-bg-info' {% if record.comprobante_id %}href='{% url 'contabilizar-comprobante' empresa record.comprobante_id %}'{% endif %} id='{{record.comprobante_id}}'>{{record.comprobante}}</a>", attrs={
        "td": {
            'class': 'text-center',
        }
    })
    descripcion = tables.TemplateColumn(template_code="<span>{{record.descripcion|truncatechars:50}}</span>")
    detalle_adicional = tables.TemplateColumn(template_code="<span>{{record.detalle_adicional|truncatechars:30}}</span>")