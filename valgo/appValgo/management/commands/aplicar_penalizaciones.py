from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from appValgo.models import CuotaMensual


class Command(BaseCommand):
    help = 'Aplica penalización a cuotas vencidas del mes actual'

    def handle(self, *args, **kwargs):
        hoy       = timezone.localdate()
        aplicadas = 0

        cuotas_pendientes = CuotaMensual.objects.filter(
            estatus               = 'pendiente',
            penalizacion_aplicada = False,
            mes                   = hoy.month,
            anio                  = hoy.year,
        ).select_related('cliente__fraccionamiento')

        for cuota in cuotas_pendientes:
            dia_limite = cuota.cliente.fraccionamiento.dia_limite_pago

            if hoy.day > dia_limite:
                cuota.penalizacion_monto    = cuota.cliente.fraccionamiento.penalizacion
                cuota.penalizacion_aplicada = True
                cuota.estatus               = 'vencido'
                cuota.save(update_fields=[
                    'penalizacion_monto',
                    'penalizacion_aplicada',
                    'estatus'
                ])
                aplicadas += 1

        self.stdout.write(
            self.style.SUCCESS(f'Penalizaciones aplicadas: {aplicadas}')
        )