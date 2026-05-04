from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Auditoria(models.Model):
    puntos_clave = models.JSONField()
    banderas_rojas = models.JSONField()
    riesgo_total = models.TextField()
    tipo = models.TextField()
    archivo = models.FileField(upload_to="contratos/%Y/%m/%d/")
    nombre_archivo = models.TextField()
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auditorias_propias")
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.TextField()
