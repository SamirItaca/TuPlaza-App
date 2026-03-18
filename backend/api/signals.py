from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Usuario, Reserva, Notificacion

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """
    Cada vez que se crea un User en Django, 
    se crea automáticamente su perfil de Usuario.
    """
    if created:
       Usuario.objects.get_or_create(user=instance)
    #para que lo obtenga o si no lo cree.
@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    """
    Si se actualiza el User, nos aseguramos de 
    que el perfil se guarde también, solo si existe.
    """
    if hasattr(instance, 'perfil'):
        instance.perfil.save()

@receiver(post_save, sender=Reserva)
def gestionar_notificaciones_reserva(sender, instance, created, **kwargs):
    """
    Gestiona el envío de notificaciones automáticas 
    según el ciclo de vida de una reserva.
    """
    # Formateo de  las fechas para que sean legibles en el mensaje
    fecha_inicio_str = instance.fecha_inicio.strftime('%d/%m/%Y %H:%M')
    fecha_fin_str = instance.fecha_fin.strftime('%d/%m/%Y %H:%M')

    if created:
        # 1. NOTIFICACIÓN AL DUEÑO con FECHAS
        Notificacion.objects.create(
            usuario=instance.garaje.propietario,
            reserva=instance,
            titulo="Nueva solicitud de reserva",
            mensaje=(
                f"El usuario {instance.usuario.user.username} quiere tu garaje en {instance.garaje.direccion}. "
                f"Desde el {fecha_inicio_str} hasta el {fecha_fin_str}."
            ),
            tipo='NUEVA_RESERVA'
        )
    else:
        # 2. NOTIFICACIÓN AL CLIENTE (Aceptada/Rechazada)
        if instance.estado == 'confirmada':
            Notificacion.objects.create(
                usuario=instance.usuario,
                reserva=instance,
                titulo="Reserva Aceptada",
                mensaje=f"¡Confirmado! Tu reserva en {instance.garaje.direccion} para el {fecha_inicio_str} ha sido aceptada.",
                tipo='RESERVA_ACEPTADA'
            )
        elif instance.estado == 'cancelada':
            Notificacion.objects.create(
                usuario=instance.usuario,
                reserva=instance,
                titulo="Reserva Rechazada",
                mensaje=f"Lo sentimos, tu solicitud para el {fecha_inicio_str} ha sido rechazada.",
                tipo='RESERVA_RECHAZADA'
            )