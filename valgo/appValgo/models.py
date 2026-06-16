from django.db import models
from django_resized import ResizedImageField #Liberia pip install django-resized para optimizar imágenes
from decimal import Decimal
from django.utils import timezone

# --- MODELO DE USUARIOS (Para vendedores) ---
class Usuarios(models.Model):
    ESTATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
    ]

    id_usuario = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=255)
    nombre_usuario = models.CharField("Usuario para Login", max_length=40, unique=True, null=True)
    contraseña = models.CharField(max_length=40, null=True)
    estatus_usuario = models.CharField(max_length=2, choices=ESTATUS_CHOICES, default='A')
    
    class Meta:
        verbose_name = "Usuario de Venta"
        verbose_name_plural = "Usuarios de Venta"

    def __str__(self):
        return f"{self.nombre_usuario} - {self.nombres}"
    
    





class Fraccionamiento(models.Model):
    """
    Representa un fraccionamiento (conjunto residencial).
    Cada fraccionamiento tiene su propia cuota de mantenimiento
    y sus propias reglas de penalización.
    
    Ejemplos de fraccionamientos: Toscana, Almeras, Rioja, Cienéga.
    """

    nombre = models.CharField(
        max_length=100,
        help_text="Nombre del fraccionamiento. Ej: 'Toscana', 'Almeras'"
    )

    cuota_mantenimiento = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text=(
            "Cuota mensual de mantenimiento que paga cada cliente. "
            "En Toscana todos pagan $1,070. "
            "En Almeras varía por m², pero se configura al crear al cliente."
        )
    )

    penalizacion = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('200.00'),
        help_text=(
            "Monto fijo que se suma a la cuota cuando el cliente "
            "no paga antes del día límite. Por defecto $200."
        )
    )

    dia_limite_pago = models.PositiveSmallIntegerField(
        default=10,
        help_text=(
            "Día del mes hasta el cual el cliente puede pagar sin penalización. "
            "Si hoy es día 11 o después y no ha pagado, se aplica la penalización. "
            "Por defecto es el día 10."
        )
    )

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    """
    Representa a un propietario o residente dentro de un fraccionamiento.
    Cada cliente tiene una referencia única que se usa para identificar
    sus pagos bancarios (SPEI, depósito, etc.).

    La referencia se genera automáticamente al guardar por primera vez,
    con el formato: FRACC{id_fraccionamiento}-{id_cliente:04d}
    Ejemplo: FRACC1-0042
    """

    fraccionamiento = models.ForeignKey(
        Fraccionamiento,
        on_delete=models.PROTECT,       # no permite borrar un fraccionamiento si tiene clientes
        related_name='clientes',
        help_text="Fraccionamiento al que pertenece este cliente."
    )

    nombre = models.CharField(
        max_length=150,
        help_text="Nombre completo del propietario. Ej: 'OMAR ALVAREZ SOLIS'"
    )

    numero_lote = models.CharField(
        max_length=20,
        help_text="Número de lote dentro de la manzana. Ej: '1', '13 Y 14'"
    )

    manzana = models.CharField(
        max_length=20,
        blank=True,
        help_text="Número o identificador de manzana. Ej: '1', '2'. Puede quedar vacío."
    )

    andar = models.CharField(
        max_length=50,
        blank=True,
        help_text=(
            "Nombre del andar dentro del fraccionamiento (aplica en Almeras). "
            "Ej: 'DE LA PIEDRA', 'DEL ARBOL', 'DE LAS HOJAS'. "
            "Puede quedar vacío si el fraccionamiento no maneja andares."
        )
    )

    telefono = models.CharField(
        max_length=20,
        blank=True,
        help_text="Teléfono de contacto del propietario. Opcional."
    )

    email = models.EmailField(
        blank=True,
        help_text="Correo electrónico del propietario. Opcional. Útil para enviar estados de cuenta."
    )

    referencia = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        help_text=(
            "Clave única de este cliente para identificar sus pagos bancarios. "
            "Se genera automáticamente. Ejemplo: 'FRACC1-0042'. "
            "El cliente usará esta referencia al hacer su SPEI o depósito."
        )
    )

    activo = models.BooleanField(
        default=True,
        help_text=(
            "Indica si el cliente está activo. "
            "Un cliente inactivo no genera cuotas nuevas cada mes. "
            "Útil para casas que aún no han sido entregadas o propietarios que se fueron."
        )
    )

    fecha_entrega = models.DateField(
        null=True,
        blank=True,
        help_text=(
            "Fecha en que se entregó la casa al propietario. "
            "A partir de esta fecha el cliente empieza a generar cuotas. "
            "Corresponde a la columna 'FECHA DE ENTREGA' de tu Excel."
        )
    )

    def save(self, *args, **kwargs):
        """
        Sobreescribimos save() para generar la referencia automáticamente
        la primera vez que se crea el cliente.

        Necesitamos guardar primero para obtener el ID asignado por la base de datos,
        y luego guardamos de nuevo solo actualizando el campo 'referencia'.
        """
        super().save(*args, **kwargs)
        if not self.referencia:
            self.referencia = f"FRACC{self.fraccionamiento_id}-{self.id:04d}"
            super().save(update_fields=['referencia'])

    def __str__(self):
        return f"{self.nombre} | Lote {self.numero_lote}"


class CuotaMensual(models.Model):
    """
    Representa el cobro de mantenimiento de UN cliente para UN mes específico.

    Cada mes el sistema genera automáticamente una CuotaMensual por cliente activo.
    Inicialmente queda en estatus 'pendiente'. Cuando el banco confirma el pago,
    se actualiza a 'pagado'.

    Si el día 11 llega y el cliente no ha pagado, se marca como 'vencido'
    y se suma la penalización.

    Flujo normal:
        1. Día 1 del mes → sistema crea CuotaMensual con estatus='pendiente'
        2. Cliente paga antes del día 10 → estatus='pagado', sin penalización
        3. Si no paga al día 11 → estatus='vencido', se suma penalizacion_monto
        4. Cliente paga después del día 10 → estatus='pagado', penalización incluida
    """

    ESTATUS = [
        ('pendiente', 'Pendiente'),   # generada, esperando pago
        ('pagado',    'Pagado'),       # banco confirmó el pago
        ('vencido',   'Vencido'),      # pasó el día límite sin pagar
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,     # no permite borrar un cliente si tiene cuotas
        related_name='cuotas',
        help_text="Cliente al que pertenece esta cuota."
    )

    mes = models.PositiveSmallIntegerField(
        help_text="Mes al que corresponde esta cuota. Número del 1 al 12."
    )

    anio = models.PositiveSmallIntegerField(
        help_text="Año al que corresponde esta cuota. Ejemplo: 2025."
    )

    monto_base = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text=(
            "Monto de la cuota antes de penalización. "
            "Se copia del fraccionamiento al generar la cuota, "
            "así si la cuota sube el próximo mes, los registros anteriores no cambian."
        )
    )

    penalizacion_aplicada = models.BooleanField(
        default=False,
        help_text=(
            "Indica si ya se aplicó la penalización por atraso. "
            "Evita aplicarla dos veces al mismo mes."
        )
    )

    penalizacion_monto = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=(
            "Monto de la penalización aplicada. "
            "Normalmente $200, pero se guarda aquí por si cambia en el futuro. "
            "Es $0.00 si el cliente pagó a tiempo."
        )
    )

    fecha_pago = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha en que el banco confirmó el pago. Vacío si aún no ha pagado."
    )

    monto_pagado = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=(
            "Monto exacto que depositó el cliente según el banco. "
            "Puede diferir ligeramente del monto_total (redondeos, pagos parciales). "
            "Vacío si aún no ha pagado."
        )
    )

    estatus = models.CharField(
        max_length=20,
        choices=ESTATUS,
        default='pendiente',
        help_text="Estado actual de esta cuota."
    )

    notas = models.TextField(
        blank=True,
        help_text=(
            "Campo libre para observaciones manuales. "
            "Ej: 'Cliente llamó para avisar que paga el lunes', "
            "'Pago anual adelantado', 'Ver factura adjunta'."
        )
    )

    class Meta:
        # Un cliente no puede tener dos cuotas del mismo mes y año
        unique_together = ('cliente', 'mes', 'anio')
        # Al listar cuotas, mostrar primero las más recientes
        ordering = ['-anio', '-mes']

    @property
    def monto_total(self):
        """
        Monto que el cliente debe pagar en total, incluyendo penalización si aplica.
        Ejemplo: monto_base=$1,070 + penalizacion_monto=$200 = $1,270
        """
        return self.monto_base + self.penalizacion_monto

    @property
    def saldo_pendiente(self):
        """
        Lo que aún debe el cliente.
        Si ya pagó → $0.
        Si no ha pagado nada → monto_total completo.
        Si pagó parcial → la diferencia.

        Esto cubre el caso de tu Excel donde a veces el cliente
        paga un monto diferente al esperado.
        """
        if self.estatus == 'pagado':
            return Decimal('0.00')
        pagado = self.monto_pagado or Decimal('0.00')
        return self.monto_total - pagado

    def __str__(self):
        return f"{self.cliente} | {self.mes}/{self.anio} | {self.estatus}"
