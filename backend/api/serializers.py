from rest_framework import serializers
from .models import Usuario, Garaje, Reserva, Pago, Resena, FotoGaraje

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'telefono', 'verificado'] 

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'


class ResenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resena
        fields = '__all__'


class FotoGarajeSerializer(serializers.ModelSerializer):
      class Meta:
        model = FotoGaraje
        fields = '__all__'


class GarajeSerializer(serializers.ModelSerializer):
    propietario_detalle = UsuarioSerializer(source='propietario', read_only=True)
    fotos = FotoGarajeSerializer(many=True, read_only=True)
    resenas = ResenaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Garaje
        fields = [
            'id', 'descripcion', 'precio', 'disponible', 
            'propietario', 'propietario_detalle', 'fotos', 'resenas'
        ]