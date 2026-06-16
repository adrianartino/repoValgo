from django.contrib import admin
from django.utils.html import format_html
from .models import Usuarios, Fraccionamiento, Cliente, CuotaMensual

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre_usuario', 'nombres', 'estatus_usuario')
    list_filter = ('estatus_usuario',)
    search_fields = ('nombre_usuario', 'nombres')

@admin.register(Fraccionamiento)
class FraccionamientoAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'cuota_mantenimiento', 'penalizacion', 'dia_limite_pago']
    search_fields = ['nombre']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display   = ['nombre', 'fraccionamiento', 'numero_lote', 'andar', 'referencia', 'activo']
    list_filter    = ['fraccionamiento', 'activo']
    search_fields  = ['nombre', 'referencia', 'numero_lote']
    readonly_fields = ['referencia']  # no se edita a mano, se genera automático


@admin.register(CuotaMensual)
class CuotaMensualAdmin(admin.ModelAdmin):
    list_display  = ['cliente', 'mes', 'anio', 'monto_base', 'penalizacion_monto', 'monto_total', 'estatus']
    list_filter   = ['estatus', 'anio', 'mes', 'cliente__fraccionamiento']
    search_fields = ['cliente__nombre', 'cliente__referencia']
    readonly_fields = ['penalizacion_monto', 'penalizacion_aplicada']  # solo el sistema los modifica
