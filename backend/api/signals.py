from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Usuario

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