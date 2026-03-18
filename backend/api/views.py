from rest_framework import viewsets, generics, permissions, status
from .models import Usuario, Garaje, Reserva, Pago , Resena, FotoGaraje, Favorito
from .serializers import UsuarioSerializer, GarajeSerializer, ReservaSerializer, PagoSerializer, ResenaSerializer, FotoGarajeSerializer, RegistroSerializer, FavoritoSerializer
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

class FotoGarajeViewSet(viewsets.ModelViewSet):
    queryset = FotoGaraje.objects.all()
    serializer_class = FotoGarajeSerializer