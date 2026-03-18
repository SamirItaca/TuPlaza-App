from rest_framework import serializers
from .models import Usuario, Garaje, Reserva, Pago, Resena, FotoGaraje, Favorito
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'telefono', 'verificado'] 

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'
        read_only_fields = ['precio_total', 'usuario']

    def validate(self, data):
        # Creamos una instancia temporal para ejecutar el método clean() del modelo
        instance = Reserva(**data)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict if hasattr(e, 'message_dict') else e.messages)
        return data


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
            'propietario', 'propietario_detalle', 'fotos', 'resenas','activo'
        ]


class RegistroSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True)
    
    # Añadimos los campos que necesita tu modelo 'Usuario'
    telefono = serializers.CharField(write_only=True, required=False)
    tipo_usuario = serializers.CharField(write_only=True, default='Arrendatario')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'telefono', 'tipo_usuario']

    def create(self, validated_data):
       
        telefono = validated_data.pop('telefono', '')
        tipo_usuario = validated_data.pop('tipo_usuario', 'Arrendatario')

        # Creamr el User de Django (Autenticación)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        # CREAMOS EL PERFIL (Usuario) vinculado al User recién creado
    
        Usuario.objects.create(
            user=user,
            nombre=f"{user.first_name} {user.last_name}".strip() or user.username,
            email=user.email,
            telefono=telefono,
            tipo_usuario=tipo_usuario
        )

        return user

# para mostrar datos del perfil
class UsuarioPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
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
