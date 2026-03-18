from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator # IMPORTANTE
from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image
import io, os
from datetime import timedelta

# 1. Usuarios (Perfil extendido)
class Usuario(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='perfil'
    )
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # Nota: El password ya lo maneja settings.AUTH_USER_MODEL, 
    # pero si lo necesitas para el registro manual está bien.
    telefono = models.CharField(max_length=20, blank=True)
    tipo_usuario = models.CharField(max_length=50) # Arrendador/Arrendatario
    verificado = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# 2. Garajes 
class Garaje(models.Model):
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='garajes')
    descripcion = models.TextField()
    precio = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)] 
    )
    disponible = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.direccion} - {self.precio}€/día"

# 3. Reservas 
class Reserva(models.Model):
    garaje = models.ForeignKey(Garaje, on_delete=models.CASCADE)
    # Corregido: Apuntamos al modelo Usuario que definiste arriba
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    estado = models.CharField(
        max_length=20, 
        choices=[
            ('pendiente', 'Pendiente'),
            ('confirmada', 'Confirmada'),
            ('cancelada', 'Cancelada')
        ],
        default='pendiente'
    )

    def clean(self):
        super().clean()
        
        if not self.fecha_inicio or not self.fecha_fin:
            return

        # 1. Validación de orden de fechas
        if self.fecha_fin <= self.fecha_inicio:
            raise ValidationError("La fecha de fin debe ser posterior a la de inicio.")

        # 2. Reserva mínima de 24 horas (usando segundos para precisión)
        duracion = self.fecha_fin - self.fecha_inicio
        if duracion.total_seconds() < 86400: # 86.400 seg = 24h
            raise ValidationError("La reserva mínima debe ser de al menos 24 horas.")

        # 3. No reservar en el pasado
        if self.fecha_inicio < timezone.now():
            raise ValidationError("La reserva no puede empezar en una fecha pasada.")

        # 4. Solapamientos 
        existe_solapamiento = Reserva.objects.filter(
            garaje=self.garaje,
            fecha_inicio__lt=self.fecha_fin,
            fecha_fin__gt=self.fecha_inicio
        ).exclude(pk=self.pk).exists()

        if existe_solapamiento:
            raise ValidationError("Este garaje ya está reservado para esas fechas.")

    def save(self, *args, **kwargs):
        # Cálculo de días (siempre mínimo 1 por la validación del clean)
        duracion = self.fecha_fin - self.fecha_inicio
        segundos_totales = duracion.total_seconds()
        segundos_dia = 86400
        
        dias_completos = int(segundos_totales // segundos_dia)
    
        # Lógica: si se pasa un segundo del día, cobramos otro día
        if segundos_totales % segundos_dia > 0:
            dias_a_cobrar = dias_completos + 1
        else:
            dias_a_cobrar = dias_completos

        from decimal import Decimal

        self.precio_total = Decimal(dias_a_cobrar) * Decimal(self.garaje.precio)   
         
        self.full_clean()
        super().save(*args, **kwargs)

# 4. Fotos Garaje 
class FotoGaraje(models.Model):
    garaje = models.ForeignKey(Garaje, related_name='fotos', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='garajes/%Y/%m/%d/')
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Foto {self.id} del garaje {self.garaje.id}"

    def save(self, *args, **kwargs):
        if self.imagen:
            self.optimizar_imagen()
        super().save(*args, **kwargs)

    def optimizar_imagen(self):
        img = Image.open(self.imagen)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        if img.width > 1200:
            nuevo_ancho = 1200
            nuevo_alto = int((nuevo_ancho * img.height) / img.width)
            img = img.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=85, optimize=True)
        buffer.seek(0)

        nombre_base = os.path.splitext(self.imagen.name)[0]
        nuevo_nombre = f"{nombre_base}.jpg"
        
        # El save=False es vital para evitar bucles infinitos
        self.imagen.save(nuevo_nombre, ContentFile(buffer.getvalue()), save=False)

# 5. Pagos 
class Pago(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='pago')
    metodo_pago = models.CharField(max_length=50) 
    estado = models.CharField(max_length=20, default='pendiente') 
    fecha_pago = models.DateTimeField(auto_now_add=True)

    @property
    def monto_total(self):
        return self.reserva.precio_total

# 6. Reseñas 
class Resena(models.Model):
    garaje = models.ForeignKey(Garaje, related_name='resenas', on_delete=models.CASCADE)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    comentario = models.TextField()

# 7. Favoritos
class Favorito(models.Model):
    # Unificado para usar tu modelo Usuario
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='favoritos')
    garaje = models.ForeignKey(Garaje, on_delete=models.CASCADE, related_name='favoritos_usuarios')
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'garaje')
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'

    def __str__(self):
        return f"{self.usuario.nombre} - {self.garaje.direccion}"
    
# 8. notificaciones

class Notificacion(models.Model):
    #  tipos de avisos posibles
    TIPOS_AVISO = (
        ('NUEVA_RESERVA', 'Nueva solicitud de reserva'),
        ('RESERVA_ACEPTADA', 'Tu reserva ha sido aceptada'),
        ('RESERVA_RECHAZADA', 'Tu reserva ha sido rechazada'),
        ('MENSAJE_CHAT', 'Tienes un nuevo mensaje'), # Por si añades chat luego
    )

    # El destinatario de la notificación
    usuario = models.ForeignKey(
        'Usuario', 
        on_delete=models.CASCADE, 
        related_name='notificaciones'
    )
    
    # Relación con la reserva para que el usuario pueda ir directo a verla
    reserva = models.ForeignKey(
        'Reserva', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='notificaciones_reserva'
    )

    titulo = models.CharField(max_length=100)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS_AVISO)
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion'] # Las más nuevas primero

    def __str__(self):
        return f"{self.tipo} - {self.usuario.user.username}"