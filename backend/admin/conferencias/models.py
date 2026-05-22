import uuid
from django.db import models

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Usuario(BaseModel):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    class Meta:
        db_table = '"content"."usuario"'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Conferencia(BaseModel):
    nombre = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        db_table = '"content"."conferencia"'
        verbose_name = 'Conferencia'
        verbose_name_plural = 'Conferencias'

    def __str__(self):
        return self.nombre

class Track(BaseModel):
    conferencia = models.ForeignKey(Conferencia, on_delete=models.CASCADE, db_column='id_conferencia', related_name='tracks')
    nombre = models.CharField(max_length=255)

    class Meta:
        db_table = '"content"."track"'
        verbose_name = 'Track'
        verbose_name_plural = 'Tracks'

    def __str__(self):
        return f"{self.nombre} ({self.conferencia.nombre})"

class Ponente(BaseModel):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, db_column='id_usuario', related_name='ponente_perfil')
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = '"content"."ponente"'
        verbose_name = 'Ponente'
        verbose_name_plural = 'Ponentes'

    def __str__(self):
        return f"Ponente: {self.usuario.nombre}"

class Sesion(BaseModel):
    track = models.ForeignKey(Track, on_delete=models.CASCADE, db_column='id_track', related_name='sesiones')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField()
    capacidad = models.IntegerField(default=50)
    
    ponentes = models.ManyToManyField(Ponente, db_table='sesion_ponente', related_name='sesiones')

    class Meta:
        db_table = '"content"."sesion"'
        verbose_name = 'Sesión'
        verbose_name_plural = 'Sesiones'

    def __str__(self):
        return self.titulo

class Oyente(BaseModel):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario', related_name='sesiones_oyente')
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE, db_column='id_sesion', related_name='oyentes')

    class Meta:
        db_table = '"content"."oyente"'
        verbose_name = 'Oyente'
        verbose_name_plural = 'Oyentes'
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'sesion'], name='unique_oyente_sesion')
        ]