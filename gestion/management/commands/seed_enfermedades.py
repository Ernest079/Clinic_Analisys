from django.core.management.base import BaseCommand
from django.db import transaction
from gestion.models import Enfermedad, Sintoma, Signo, PruebaLaboratorio, PruebaPosMortem

class Command(BaseCommand):
    help = 'Carga enfermedades y sus relaciones (Síntomas, Signos, Pruebas)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Iniciando carga de Enfermedades...'))

        # Definición de la "Base de Conocimiento"
        base_conocimiento = [
            {
                "nombre": "Gripe Estacional (Influenza)",
                "descripcion": "Infección viral común que ataca el sistema respiratorio.",
                "sintomas": ["Dolor de cabeza intenso", "Fatiga crónica", "Escalofríos", "Tos seca", "Dolor muscular"],
                "signos": ["Fiebre (>38°C)", "Inflamación de garganta"],
                "pruebas": ["Hemograma Completo", "Prueba de PCR (Viral)"],
                "postmortem": []
            },
            {
                "nombre": "COVID-19",
                "descripcion": "Enfermedad respiratoria causada por el coronavirus SARS-CoV-2.",
                "sintomas": ["Pérdida del olfato", "Dificultad para respirar", "Fatiga crónica", "Tos seca"],
                "signos": ["Fiebre (>38°C)", "Cianosis (Coloración azul)"], # Cianosis si es grave
                "pruebas": ["Prueba de PCR (Viral)", "Radiografía de Tórax", "Tomografía Computarizada (TC)"],
                "postmortem": ["Autopsia Clínica Completa"]
            },
            {
                "nombre": "Diabetes Mellitus Tipo 2",
                "descripcion": "Afección crónica que afecta la manera en la que el cuerpo procesa el azúcar en sangre.",
                "sintomas": ["Visión borrosa", "Fatiga crónica", "Sed excesiva", "Micción frecuente"],
                "signos": ["Pérdida de peso rápida", "Heridas que sanan lento"],
                "pruebas": ["Prueba de Glucosa en Sangre", "Urinálisis"],
                "postmortem": []
            },
            {
                "nombre": "Hipertensión Arterial",
                "descripcion": "Presión arterial alta, conocida como el asesino silencioso.",
                "sintomas": ["Dolor de cabeza intenso", "Mareos y vértigo", "Zumbido en oídos", "Visión borrosa"],
                "signos": ["Hipertensión arterial", "Dilatación de pupilas"],
                "pruebas": ["Perfil Lipídico", "Electrocardiograma"], 
                "postmortem": ["Histopatología de Órganos"]
            },
            {
                "nombre": "Hepatitis Viral",
                "descripcion": "Inflamación del hígado causada generalmente por una infección viral.",
                "sintomas": ["Náuseas", "Dolor abdominal", "Fatiga crónica", "Pérdida de apetito"],
                "signos": ["Ictericia (Piel amarilla)", "Orina oscura"],
                "pruebas": ["Prueba de Función Hepática", "Ecografía abdominal"],
                "postmortem": ["Histopatología de Órganos"]
            }
        ]

        with transaction.atomic():
            for data in base_conocimiento:
                enfermedad, created = Enfermedad.objects.get_or_create(
                    nombre=data["nombre"],
                    defaults={"descripcion": data["descripcion"]}
                )
                
                accion = "Creada" if created else "Actualizada"
                self.stdout.write(f"- Procesando: {enfermedad.nombre} ({accion})")

                for s_nombre in data["sintomas"]:
                    obj, _ = Sintoma.objects.get_or_create(nombre=s_nombre)
                    enfermedad.sintomas.add(obj)

                for s_nombre in data["signos"]:
                    obj, _ = Signo.objects.get_or_create(nombre=s_nombre)
                    enfermedad.signos.add(obj)

                for p_nombre in data["pruebas"]:
                    obj, _ = PruebaLaboratorio.objects.get_or_create(nombre=p_nombre)
                    enfermedad.pruebas_lab.add(obj)

                for pm_nombre in data["postmortem"]:
                    obj, _ = PruebaPosMortem.objects.get_or_create(nombre=pm_nombre)
                    enfermedad.pruebas_postmortem.add(obj)

                enfermedad.save()

        self.stdout.write(self.style.SUCCESS('--------------------------------------------------'))
        self.stdout.write(self.style.SUCCESS(f'Se han procesado {len(base_conocimiento)} enfermedades con sus relaciones.'))
        self.stdout.write(self.style.SUCCESS('¡El Motor de Inferencia ahora tiene datos para trabajar! 🚀'))