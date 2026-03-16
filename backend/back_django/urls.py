"""
URL configuration for back_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings # Importante para las imágenes
from django.conf.urls.static import static # Importante para las imágenes
from api.views import (
    UsuarioViewSet, GarajeViewSet, ReservaViewSet, 
    PagoViewSet, ResenaViewSet, FotoGarajeViewSet, RegistroView, FavoritoViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


# 1. El router genera automáticamente las URLs (CRUD completo)
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'garajes', GarajeViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'pagos', PagoViewSet)
router.register(r'resenas', ResenaViewSet)
router.register(r'fotos', FotoGarajeViewSet)
router.register(r'favoritos', FavoritoViewSet, basename='favorito')

# 2. Definición de rutas principales
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), 

    #rutas para el login 

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/registro/', RegistroView.as_view(), name='registro'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', include(router.urls)),
]

# 3. Configuración para ver las fotos en el navegador durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
