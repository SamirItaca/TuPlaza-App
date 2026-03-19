from datetime import timezone

from rest_framework import serializers
from .models import Usuario, Garaje, Reserva, Pago, Resena, FotoGaraje, Favorito, Notificacion
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'telefono', 'verificado'] 

class ReservaSerializer(serializers.ModelSerializer):
    garaje_direccion = serializers.ReadOnlyField(source='garaje.direccion')
    cliente_username = serializers.ReadOnlyField(source='usuario.user.username')

    class Meta:
        model = Reserva
        fields = [
            'id', 'garaje', 'usuario', 'fecha_inicio', 'fecha_fin', 
            'estado', 'precio_total', 'garaje_direccion', 'cliente_username'
        ]
        read_only_fields = ['precio_total', 'usuario', 'estado']

    def validate(self, data):
        request = self.context.get('request')
        
        # 0. Primero comprobamos que hay una sesión activa
        if not request or not request.user.is_authenticated or not hasattr(request.user, 'perfil'):
            raise serializers.ValidationError({"auth": "Debes estar autenticado y tener un perfil para reservar."})

        user_perfil = request.user.perfil
        garaje = data.get('garaje')
        f_inicio = data.get('fecha_inicio')
        f_fin = data.get('fecha_fin')

        # 1. ¿EL GARAJE EXISTE Y ESTÁ ACTIVO?
        if not garaje.activo or not garaje.disponible:
            raise serializers.ValidationError({"garaje": "Este garaje no está aceptando reservas actualmente."})

        # 2. ¿ERES EL DUEÑO? (Seguridad Blindada)
        if garaje.propietario == user_perfil:
            raise serializers.ValidationError({"garaje": "No puedes reservar tu propio garaje."})

        # 3. ¿FECHAS EN EL PASADO?
        # (Asegúrate de que 'timezone' esté importado de 'django.utils')
        if f_inicio < timezone.now():
            raise serializers.ValidationError({"fecha_inicio": "La fecha de inicio no puede ser en el pasado."})

        # 4. ORDEN DE FECHAS
        if f_fin <= f_inicio:
            raise serializers.ValidationError({"fecha_fin": "La fecha de fin debe ser posterior a la de inicio."})

        # 5. DURACIÓN MÍNIMA (24 horas)
        duracion = f_fin - f_inicio
        if duracion.total_seconds() < 86400: 
            raise serializers.ValidationError({"fecha_fin": "La reserva debe ser de al menos 24 horas."})

        # 6. SOLAPAMIENTO (Overlapping)
        exists = Reserva.objects.filter(
            garaje=garaje,
            estado__in=['pendiente', 'confirmada'],
            fecha_inicio__lt=f_fin,
            fecha_fin__gt=f_inicio
        ).exclude(id=self.instance.id if self.instance else None).exists()

        if exists:
            raise serializers.ValidationError({"error": "El garaje ya está ocupado o solicitado en esas fechas."})

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
        # 1. Extraemos los campos extra
        telefono = validated_data.pop('telefono', '')
        tipo_usuario = validated_data.pop('tipo_usuario', 'Arrendatario')

        # 2. Creamos el User de Django
        # (Esto dispara la SIGNAL automáticamente y crea el perfil vacío)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        # 3. ACTUALIZAMOS EL PERFIL que la Signal ya ha creado
        # En lugar de .create(), usamos .filter().update() o accedemos a user.perfil
        perfil = user.perfil # Gracias a la Signal, esto ya existe
        perfil.nombre = f"{user.first_name} {user.last_name}".strip() or user.username
        perfil.email = user.email
        perfil.telefono = telefono
        perfil.tipo_usuario = tipo_usuario
        perfil.save()

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


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'titulo', 'mensaje', 'tipo', 'leida', 'fecha_creacion', 'reserva']