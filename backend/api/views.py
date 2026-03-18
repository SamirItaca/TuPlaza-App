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
        # Usamos .perfil porque Reserva apunta a tu modelo Usuario
        return Reserva.objects.filter(usuario=self.request.user.perfil)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user.perfil)

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

class ResenaViewSet(viewsets.ModelViewSet):
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer

    @action(detail=True, methods=['post'])
    def aceptar(self, request, pk=None):
        reserva = self.get_object()
        
        # SEGURIDAD: ¿Es el usuario actual el dueño del garaje?
        if reserva.garaje.propietario != request.user.perfil:
            return Response({'error': 'No tienes permiso para aceptar esta reserva'}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        reserva.estado = 'confirmada'
        reserva.save() # Esto disparará la Signal de "Reserva Aceptada" automáticamente
        return Response({'status': 'reserva confirmada'})

    @action(detail=True, methods=['post'])
    def rechazar(self, request, pk=None):
        reserva = self.get_object()
        
        # SEGURIDAD: ¿Es el usuario el dueño?
        if reserva.garaje.propietario != request.user.perfil:
            return Response({'error': 'No tienes permiso para rechazar esta reserva'}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        reserva.estado = 'cancelada'
        reserva.save() # Esto disparará la Signal de "Reserva Rechazada"
        return Response({'status': 'reserva rechazada'})
    
    @action(detail=False, methods=['get'])
    def recibidas(self, request):
        """
        Devuelve las reservas que LE HAN HECHO AL USUARIO OROS USUARIOS.
        """
        reservas = Reserva.objects.filter(garaje__propietario=request.user.perfil)
        serializer = self.get_serializer(reservas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def mis_reservas(self, request):
        """
        Devuelve las reservas que EL USUARIO  ha realizado 
       
        """
        # Filtramos por el perfil del usuario logueado
        reservas = Reserva.objects.filter(usuario=request.user.perfil).order_by('-fecha_inicio')
        
        # Usamos el serializador para devolver los datos
        page = self.paginate_queryset(reservas)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(reservas, many=True)
        return Response(serializer.data)

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

