from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from api.views import (
    UsuarioViewSet, GarajeViewSet, ReservaViewSet, 
    PagoViewSet, ResenaViewSet, FotoGarajeViewSet, RegistroView, FavoritoViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'garajes', GarajeViewSet, basename='garaje')
router.register(r'reservas', ReservaViewSet, basename='reserva')
router.register(r'pagos', PagoViewSet, basename='pago')
router.register(r'resenas', ResenaViewSet, basename='resena')
router.register(r'fotos', FotoGarajeViewSet, basename='foto')
router.register(r'favoritos', FavoritoViewSet, basename='favorito')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Casos de uso: Login y Seguridad
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Caso de uso: Crear cuenta
    path('api/registro/', RegistroView.as_view(), name='registro'),

    # Caso de uso: Documentación (Swagger)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Endpoints del Router (Usuarios, Garajes, Reservas, Favoritos...)
    path('api/', include(router.urls)), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)