from django.contrib import admin
from .models import Usuario, Garaje, Reserva, FotoGaraje, Pago, Resena

# Registro sencillo para modelos secundarios
admin.site.register(Usuario)
admin.site.register(FotoGaraje)
admin.site.register(Pago)
admin.site.register(Resena)

# Registro avanzado para Garajes (para ver columnas en la lista)
@admin.register(Garaje)
class GarajeAdmin(admin.ModelAdmin):
    list_display = ('id', 'propietario', 'precio', 'disponible')
    list_filter = ('disponible',)
    search_fields = ('descripcion', 'direccion')

# Registro avanzado para Reservas
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'garaje', 'fecha_inicio', 'estado')
    list_editable = ('estado',) # Permite cambiar el estado desde la lista

# Register your models here.
