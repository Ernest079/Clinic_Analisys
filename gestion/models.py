from django.db import models
from django.contrib.auth.models import User

# ==========================================
# 1. CATÁLOGOS Y MODELOS BASE (Independientes)
# Deben ir primero porque Enfermedad los usa
# ==========================================

class Sintoma(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    def __str__(self): return self.nombre

class Signo(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    def __str__(self): return self.nombre

class PruebaLaboratorio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    def __str__(self): return self.nombre

class PruebaPosMortem(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    def __str__(self): return self.nombre

# ==========================================
# 2. ENFERMEDAD (Depende de los catálogos)
# ==========================================

class Enfermedad(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField()
    
    # Relaciones ManyToMany
    sintomas = models.ManyToManyField(Sintoma, blank=True, related_name='enfermedades')
    signos = models.ManyToManyField(Signo, blank=True, related_name='enfermedades')
    pruebas_lab = models.ManyToManyField(PruebaLaboratorio, blank=True, related_name='enfermedades')
    pruebas_postmortem = models.ManyToManyField(PruebaPosMortem, blank=True, related_name='enfermedades')

    def __str__(self):
        return self.nombre

# ==========================================
# 3. PACIENTE (Independiente de Enfermedad)
# ==========================================

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

# ==========================================
# 4. DIAGNÓSTICO (Depende de Paciente y Enfermedad)
# ==========================================

class Diagnostico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # AHORA SÍ FUNCIONA: Enfermedad ya fue leída por Python arriba
    enfermedad_diagnosticada = models.ForeignKey(Enfermedad, on_delete=models.SET_NULL, null=True)
    
    # Estas relaciones son opcionales aquí porque ya están definidas en la enfermedad,
    # pero las mantenemos si quieres guardar qué síntomas ESPECÍFICOS tuvo este paciente.
    sintomas_presentados = models.ManyToManyField(Sintoma, blank=True)
    pruebas_realizadas = models.ManyToManyField(PruebaLaboratorio, blank=True)
    
    notas_adicionales = models.TextField(blank=True, null=True)
    fecha_diagnostico = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnóstico de {self.paciente} - {self.fecha_diagnostico.strftime('%Y-%m-%d')}"

# ==========================================
# 5. TRATAMIENTO (Depende de Diagnóstico)
# ==========================================

class Tratamiento(models.Model):
    diagnostico = models.ForeignKey(Diagnostico, on_delete=models.CASCADE, related_name='tratamientos')
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Tratamiento para {self.diagnostico.paciente}"