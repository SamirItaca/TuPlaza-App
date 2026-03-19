from rest_framework import viewsets, generics, permissions, status
from .models import Usuario, Garaje, Reserva, Pago , Resena, FotoGaraje, Favorito, Notificacion
from .serializers import UsuarioSerializer, GarajeSerializer, ReservaSerializer, PagoSerializer, ResenaSerializer, FotoGarajeSerializer, RegistroSerializer, FavoritoSerializer, NotificacionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import ScopedRateThrottle

# 1. Usuarios: Cada uno gestiona SOLO su perfil
class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Evitamos que un usuario vea los perfiles de otros
        return Usuario.objects.filter(user=self.request.user)

# 2. Garajes: Filtrado para el público
class GarajeViewSet(viewsets.ModelViewSet):
    serializer_class = GarajeSerializer
    
    def get_queryset(self):
        return Garaje.objects.filter(activo=True, disponible=True)

# 3. Reservas: Uso de .perfil
class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Reservas hechas por mí como cliente
        return Reserva.objects.filter(usuario=self.request.user.perfil)

    def perform_create(self, serializer):
        # Forzamos que el usuario de la reserva sea el que está logueado
        serializer.save(usuario=self.request.user.perfil)

    @action(detail=True, methods=['post'])
    def aceptar(self, request, pk=None):
        reserva = self.get_object()
        
        # 1. Seguridad: ¿Eres el dueño?
        if reserva.garaje.propietario != request.user.perfil:
            return Response({'error': 'No tienes permiso'}, status=status.HTTP_403_FORBIDDEN)
        
        # 2. Validación extra: ¿Sigue el garaje libre en esas fechas?
        # (Llamamos al método clean del modelo que ya tiene la lógica de solapamiento)
        try:
            reserva.estado = 'confirmada'
            reserva.full_clean() # Esto dispara el método clean() del modelo
            reserva.save()
            return Response({'status': 'reserva confirmada'})
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def rechazar(self, request, pk=None):
        reserva = self.get_object()
        if reserva.garaje.propietario != request.user.perfil:
            return Response({'error': 'No eres el dueño'}, status=status.HTTP_403_FORBIDDEN)
        reserva.estado = 'cancelada'
        reserva.save()
        return Response({'status': 'reserva rechazada'})

class ResenaViewSet(viewsets.ModelViewSet):
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer
    permission_classes = [IsAuthenticated]

# 4. Registro: Con protección de tasa (Throttling)
class RegistroView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny] 
    serializer_class = RegistroSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'registros'

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Usuario creado correctamente",
            "user": response.data
        }, status=status.HTTP_201_CREATED)

# 5. Favoritos: Corregido el acceso al perfil
class FavoritoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]
    serializer_class = FavoritoSerializer

    def get_queryset(self):
        # IMPORTANTE: Filtrar por el perfil relacionado, no por el User de Django
        return Favorito.objects.filter(usuario=self.request.user.perfil)

    def perform_create(self, serializer):
        # IMPORTANTE: Guardar vinculando al perfil
        serializer.save(usuario=self.request.user.perfil)

    @action(detail=False, methods=['delete'], url_path='borrar-por-garaje/(?P<garaje_id>[^/.]+)')
    def borrar_por_garaje(self, request, garaje_id=None):
        # Buscamos usando el perfil del usuario logueado
        favorito = Favorito.objects.filter(
            usuario=request.user.perfil, 
            garaje_id=garaje_id
        ).first()

        if favorito:
            favorito.delete()
            return Response({'detail': 'Favorito eliminado.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)

# Viewsets simples (puedes añadirles IsAuthenticated si quieres)
class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

class FotoGarajeViewSet(viewsets.ModelViewSet):
    queryset = FotoGaraje.objects.all()
    serializer_class = FotoGarajeSerializer

class NotificacionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para ver y gestionar notificaciones.
    Es ReadOnly porque las notificaciones se crean solas por Signals.
    """
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Solo devolvemos las notificaciones del usuario que está logueado
        return Notificacion.objects.filter(usuario=self.request.user.perfil)

    # Acción para marcar UNA notificación como leída
    @action(detail=True, methods=['post'])
    def marcar_leida(self, request, pk=None):
        notificacion = self.get_object()
        notificacion.leida = True
        notificacion.save()
        return Response({'status': 'notificación leída'})

    # Acción para marcar TODAS como leídas de golpe (útil para el Front)
    @action(detail=False, methods=['post'])
    def marcar_todas_leidas(self, request):
        self.get_queryset().update(leida=True)
        return Response({'status': 'todas las notificaciones marcadas como leídas'})

