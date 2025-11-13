from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Enfermedad(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    
class Sintoma(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    enfermedades = models.ManyToManyField(Enfermedad, related_name='sintomas')

    def __str__(self):
        return self.nombre

class PruebaLaboratorio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    enfermedades = models.ManyToManyField(Enfermedad, related_name='pruebas_laboratorio')
    
    def __str__(self):
        return self.nombre
    
class Diagnostico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # El User que hace el diagnóstico
    enfermedad_diagnosticada = models.ForeignKey(Enfermedad, on_delete=models.SET_NULL, null=True)
    sintomas_presentados = models.ManyToManyField(Sintoma, blank=True)
    pruebas_realizadas = models.ManyToManyField(PruebaLaboratorio, blank=True)
    notas_adicionales = models.TextField(blank=True, null=True)
    fecha_diagnostico = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnóstico de {self.paciente} - {self.fecha_diagnostico.strftime('%Y-%m-%d')}"

# Modelo para el Tratamiento
class Tratamiento(models.Model):
    diagnostico = models.ForeignKey(Diagnostico, on_delete=models.CASCADE, related_name='tratamientos')
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Tratamiento para {self.diagnostico.paciente}"