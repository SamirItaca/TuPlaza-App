from rest_framework import serializers
from .models import Usuario, Garaje, Reserva, Pago, Resena, FotoGaraje
from django.contrib.auth.models import User

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


class RegistroSerializer(serializers.ModelSerializer):

    """
    Maneja la creación de usuarios encriptando la contraseña 
    mediante el método create_user de Django.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password'] # Campos base de Django

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

# Este lo usaremos luego para mostrar datos del perfil
class UsuarioPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = User # O tu modelo Usuario si lo vinculamos
        fields = ['id', 'username', 'email']