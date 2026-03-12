from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Usuarios 
class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True)
    tipo_usuario = models.CharField(max_length=50) # Arrendador/Arrendatario
    verificado = models.BooleanField(default=False)

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
class FotoGaraje(models.Model):
    garaje = models.ForeignKey(Garaje, on_delete=models.CASCADE, related_name='fotos')
    id_imagen = models.CharField(max_length=255) 

# 5. Pagos 
class Pago(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=50)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)

# 6. Reseñas 
class Resena(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    comentario = models.TextField()