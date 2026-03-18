from rest_framework import viewsets, generics, permissions, status
from .models import Usuario, Garaje, Reserva, Pago , Resena, FotoGaraje, Favorito
from .serializers import UsuarioSerializer, GarajeSerializer, ReservaSerializer, PagoSerializer, ResenaSerializer, FotoGarajeSerializer, RegistroSerializer, FavoritoSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class GarajeViewSet(viewsets.ModelViewSet):
    queryset = Garaje.objects.all()
    serializer_class = GarajeSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

class ResenaViewSet(viewsets.ModelViewSet):
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer

class FotoGarajeViewSet(viewsets.ModelViewSet):
    queryset = FotoGaraje.objects.all()
    serializer_class = FotoGarajeSerializer

class RegistroView(generics.CreateAPIView):
    queryset = User.objects.all()
    # Importante: AllowAny permite que alguien que NO tiene cuenta pueda entrar a crear una
    permission_classes = [AllowAny] 
    serializer_class = RegistroSerializer

   
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Usuario creado correctamente",
            "user": response.data
        }, status=status.HTTP_201_CREATED)

class FavoritoViewSet(viewsets.ModelViewSet):
    # Esto obliga a que el Interceptor de Angular envíe el Token
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication] # Opcional si está en settings.py
    serializer_class = FavoritoSerializer

    def get_queryset(self):
        # El interceptor permite que 'self.request.user' no sea AnonymousUser
        return Favorito.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['delete'], url_path='borrar-por-garaje/(?P<garaje_id>[^/.]+)')
    def borrar_por_garaje(self, request, garaje_id=None):
        usuario = request.user
        
        # Buscamos el favorito que coincida con el usuario y el ID del garaje
        favorito = Favorito.objects.filter(usuario=usuario, garaje_id=garaje_id).first()

        if favorito:
            favorito.delete()
            return Response({'detail': 'Favorito eliminado correctamente.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'No se encontró el favorito para este garaje.'}, status=status.HTTP_404_NOT_FOUND)
        

