from django.contrib import admin
from .models import Usuario, Conferencia, Track, Ponente, Sesion, Oyente

class TrackInline(admin.TabularInline):
    model = Track
    extra = 1

class SesionInline(admin.TabularInline):
    model = Sesion
    extra = 1
    filter_horizontal = ('ponentes',)

@admin.register(Conferencia)
class ConferenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin')
    search_fields = ('nombre',)
    list_filter = ('fecha_inicio',)
    inlines = [TrackInline]

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'conferencia')
    search_fields = ('nombre', 'conferencia__nombre')
    list_filter = ('conferencia',)
    inlines = [SesionInline]

@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'track', 'hora_inicio', 'hora_fin', 'capacidad')
    search_fields = ('titulo', 'track__nombre')
    list_filter = ('track__conferencia', 'hora_inicio')
    filter_horizontal = ('ponentes',)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'fecha_creacion')
    search_fields = ('nombre', 'apellido')

@admin.register(Ponente)
class PonenteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'descripcion')
    search_fields = ('usuario__nombre', 'usuario__apellido')

@admin.register(Oyente)
class OyenteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'sesion', 'fecha_creacion')
    search_fields = ('usuario__nombre', 'sesion__titulo')
    list_filter = ('fecha_creacion',)
    raw_id_fields = ('usuario', 'sesion')