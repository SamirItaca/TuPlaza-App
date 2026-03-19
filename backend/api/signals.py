from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Usuario, Reserva, Notificacion

@receiver(post_save, sender=User)
def manejar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        # get_or_create evita errores si por algún motivo el perfil ya existía
        Usuario.objects.get_or_create(user=instance)
    else:
        # Solo guardamos si el perfil existe para evitar errores en el admin o consola
        if hasattr(instance, 'perfil'):
            instance.perfil.save()

@receiver(post_save, sender=Reserva)
def gestionar_notificaciones_reserva(sender, instance, created, **kwargs):
    f_inicio = instance.fecha_inicio.strftime('%d/%m/%Y a las %H:%M')
    f_fin = instance.fecha_fin.strftime('%d/%m/%Y a las %H:%M')

    if created:
        # NOTIFICACIÓN AL DUEÑO: Ahora incluimos las fechas en el mensaje
        Notificacion.objects.create(
            usuario=instance.garaje.propietario,
            reserva=instance,
            titulo="Nueva solicitud de reserva",
            mensaje=(
                f"El usuario {instance.usuario.user.username} quiere tu garaje en {instance.garaje.direccion}.\n"
                f"Entrada: {f_inicio}\n"
                f"Salida: {f_fin}"
            ),
            tipo='NUEVA_RESERVA'
        )
    else:
        # NOTIFICACIONES AL CLIENTE (Aceptada/Rechazada)
        if instance.estado == 'confirmada':
            if not Notificacion.objects.filter(reserva=instance, tipo='RESERVA_ACEPTADA').exists():
                Notificacion.objects.create(
                    usuario=instance.usuario,
                    reserva=instance,
                    titulo="Reserva Aceptada",
                    mensaje=(
                        f"¡Confirmado! Tu reserva en {instance.garaje.direccion} ha sido aceptada.\n"
                        f"Horario: Desde el {f_inicio} hasta el {f_fin}."
                    ),
                    tipo='RESERVA_ACEPTADA'
                )
        elif instance.estado == 'cancelada':
            if not Notificacion.objects.filter(reserva=instance, tipo='RESERVA_RECHAZADA').exists():
                Notificacion.objects.create(
                    usuario=instance.usuario,
                    reserva=instance,
                    titulo="Reserva Rechazada",
                    mensaje=f"Lo sentimos, tu solicitud para el {f_inicio} ha sido rechazada por el propietario.",
                    tipo='RESERVA_RECHAZADA'
                )