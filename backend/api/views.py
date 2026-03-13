from rest_framework import viewsets, generics
from .models import Usuario, Garaje, Reserva, Pago , Resena, FotoGaraje
from .serializers import UsuarioSerializer, GarajeSerializer, ReservaSerializer, PagoSerializer, ResenaSerializer, FotoGarajeSerializer, RegistroSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

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