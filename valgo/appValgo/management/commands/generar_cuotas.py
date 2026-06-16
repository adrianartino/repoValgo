from django.core.management.base import BaseCommand
from django.utils import timezone
from appValgo.models import Cliente, CuotaMensual


class Command(BaseCommand):
    help = 'Genera las cuotas del mes actual para todos los clientes activos'

    def handle(self, *args, **kwargs):
        hoy         = timezone.localdate()
        mes_actual  = hoy.month
        anio_actual = hoy.year
        creadas     = 0
        omitidas    = 0

        clientes = Cliente.objects.filter(
            activo=True,
            fecha_entrega__lte=hoy
        ).select_related('fraccionamiento')

        for cliente in clientes:
            cuota, fue_creada = CuotaMensual.objects.get_or_create(
                cliente = cliente,
                mes     = mes_actual,
                anio    = anio_actual,
                defaults = {
                    'monto_base': cliente.fraccionamiento.cuota_mantenimiento,
                    'estatus'   : 'pendiente',
                }
            )
            if fue_creada:
                creadas += 1
            else:
                omitidas += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Cuotas generadas: {creadas} | Ya existían: {omitidas}'
            )
        )