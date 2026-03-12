from rest_framework import serializers
from .models import Usuario, Garaje, Reserva

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'telefono', 'verificado'] 

class GarajeSerializer(serializers.ModelSerializer):
    # Esta línea permite que Angular reciba los datos del dueño, no solo su ID
    propietario_detalle = UsuarioSerializer(source='propietario', read_only=True)
    
    class Meta:
        model = Garaje
        fields = [
            'id', 'descripcion', 'precio', 'disponible', 
            'propietario', 'propietario_detalle'
        ] 

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'