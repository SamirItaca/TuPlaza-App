from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from PIL import Image
import io,os
from django.core.files.base import ContentFile

# 1. Usuarios 
class Usuario(models.Model):
    # Esto vincula el modelo con el sistema de autenticación de Django
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='perfil'
    )

    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True)
    tipo_usuario = models.CharField(max_length=50) # Arrendador/Arrendatario
    verificado = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# 2. Garajes 
class Garaje(models.Model):
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='garajes')
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    # Ubicación (añadido por lógica de proyecto)
    direccion = models.CharField(max_length=255)

# 3. Reservas 
class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    garaje = models.ForeignKey(Garaje, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.CharField(max_length=50, default='pendiente')

# 4. Fotos Garaje 

def validar_tamano_foto(file):
    # Límite de 2 Megabytes
    limite_megabytes = 2.0
    if file.size > limite_megabytes * 1024 * 1024:
        raise ValidationError(f"La imagen no puede pesar más de {limite_megabytes}MB")
class FotoGaraje(models.Model):
    garaje = models.ForeignKey(Garaje, related_name='fotos', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='garajes/%Y/%m/%d/')
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Foto {self.id} del garaje {self.garaje.id}"

    def save(self, *args, **kwargs):
        # Solo procesamos si hay una imagen nueva o modificada
        if self.imagen and not self.id: # Solo al crear (o si quieres siempre, quita "and not self.id")
            self.optimizar_imagen()
        super().save(*args, **kwargs)

    def optimizar_imagen(self):
        # 1. Abrir la imagen subida
        img = Image.open(self.imagen)
        
        # 2. Convertir a RGB (necesario para guardar como JPEG si viene de PNG/otros)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # 3. Redimensionar si es más ancha de 1200px (manteniendo proporción)
        if img.width > 1200:
            nuevo_ancho = 1200
            nuevo_alto = int((nuevo_ancho * img.height) / img.width)
            img = img.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

        # 4. Comprimir en memoria
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=85, optimize=True)
        buffer.seek(0)

        # 5. Reemplazar el archivo original por el optimizado
        # Cambiamos la extensión a .jpg ya que lo hemos convertido
        nombre_base = os.path.splitext(self.imagen.name)[0]
        nuevo_nombre = f"{nombre_base}.jpg"
        
        self.imagen.save(nuevo_nombre, ContentFile(buffer.getvalue()), save=False)

    # def __str__(self):
    #     return f"Foto de {self.garaje.direccion}"


# 5. Pagos 
class Pago(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=50)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)

# 6. Reseñas 
class Resena(models.Model):
    garaje = models.ForeignKey(Garaje, related_name='resenas', on_delete=models.CASCADE)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    comentario = models.TextField()


class Favorito(models.Model):
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='favoritos')
    garaje = models.ForeignKey('Garaje', on_delete=models.CASCADE, related_name='favoritos_usuarios')
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Esto evita que un usuario guarde el mismo garaje dos veces
        unique_together = ('usuario', 'garaje')
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'

    def __str__(self):
        return f"{self.usuario.username} - {self.garaje.nombre}"