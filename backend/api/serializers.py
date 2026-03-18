from rest_framework import serializers
from .models import Usuario, Garaje, Reserva, Pago, Resena, FotoGaraje, Favorito
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

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

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    # La contraseña solo se envía (write), nunca se devuelve en el JSON (read)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        # El método create_user se encarga de hashear la contraseña
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

# Este lo usaremos luego para mostrar datos del perfil
class UsuarioPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = User # O tu modelo Usuario si lo vinculamos
        fields = ['id', 'username', 'email']


class FavoritoSerializer(serializers.ModelSerializer):
    # El usuario se asignará automáticamente en la vista, no lo pedimos en el JSON
    usuario = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = Favorito
        fields = ['id', 'usuario', 'garaje', 'fecha_agregado']

    def validate(self, data):
        # Validación extra: ¿Ya existe este favorito para este usuario?
        user = self.context['request'].user
        if Favorito.objects.filter(usuario=user, garaje=data['garaje']).exists():
            raise serializers.ValidationError("Este garaje ya está en tus favoritos.")
        return data
