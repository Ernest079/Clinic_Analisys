from django.core.management.base import BaseCommand
from gestion.models import Sintoma, Signo, PruebaLaboratorio, PruebaPosMortem

class Command(BaseCommand):
    help = 'Carga datos iniciales (Seed) para los catálogos médicos'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Iniciando carga de catálogos...'))

        # --- 1. SÍNTOMAS (Lo que siente el paciente - Subjetivo) ---
        sintomas = [
            "Dolor de cabeza intenso", "Mareos y vértigo", "Náuseas", "Fatiga crónica",
            "Visión borrosa", "Dolor abdominal", "Pérdida del olfato", "Dificultad para respirar",
            "Dolor en las articulaciones", "Insomnio", "Ansiedad", "Escalofríos"
        ]
        
        for nombre in sintomas:
            Sintoma.objects.get_or_create(nombre=nombre)
        self.stdout.write(self.style.SUCCESS(f'✔ {len(sintomas)} Síntomas cargados.'))

        # --- 2. SIGNOS (Lo que mide el médico - Objetivo) ---
        signos = [
            "Fiebre (>38°C)", "Erupción cutánea", "Taquicardia", "Hipertensión arterial",
            "Inflamación de ganglios", "Ictericia (Piel amarilla)", "Edema (Hinchazón)",
            "Cianosis (Coloración azul)", "Dilatación de pupilas", "Pérdida de peso rápida"
        ]

        for nombre in signos:
            Signo.objects.get_or_create(nombre=nombre)
        self.stdout.write(self.style.SUCCESS(f'✔ {len(signos)} Signos cargados.'))

        # --- 3. PRUEBAS DE LABORATORIO ---
        pruebas_lab = [
            "Hemograma Completo", "Prueba de Glucosa en Sangre", "Perfil Lipídico",
            "Prueba de Función Hepática", "Urinálisis", "Cultivo de Garganta",
            "Radiografía de Tórax", "Tomografía Computarizada (TC)", "Resonancia Magnética",
            "Prueba de PCR (Viral)", "Biopsia de Tejido"
        ]   

        for nombre in pruebas_lab:
            PruebaLaboratorio.objects.get_or_create(nombre=nombre)
        self.stdout.write(self.style.SUCCESS(f'✔ {len(pruebas_lab)} Pruebas de Laboratorio cargadas.'))

        # --- 4. PRUEBAS POS-MORTEM ---
        pruebas_pm = [
            "Autopsia Clínica Completa", "Examen Toxicológico", "Histopatología de Órganos",
            "Análisis de ADN Post-mortem", "Examen Dental Forense", "Datación de Restos",
            "Cultivo Microbiológico Post-mortem"
        ]

        for nombre in pruebas_pm:
            PruebaPosMortem.objects.get_or_create(nombre=nombre)
        self.stdout.write(self.style.SUCCESS(f'✔ {len(pruebas_pm)} Pruebas Pos-mortem cargadas.'))

        self.stdout.write(self.style.SUCCESS('--------------------------------------'))
        self.stdout.write(self.style.SUCCESS('¡Base de datos alimentada correctamente!'))