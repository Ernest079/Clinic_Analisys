from django.db import migrations
from django.contrib.auth.hashers import make_password

def crear_datos_iniciales(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Group = apps.get_model('auth', 'Group')
    Paciente = apps.get_model('gestion', 'Paciente') # Tu modelo Paciente

    # 1. Crear Grupo Medicos
    grupo_medicos, created = Group.objects.get_or_create(name='Medicos')

    # 2. Crear un Usuario Médico (si no existe)
    if not User.objects.filter(username='doctor1').exists():
        doctor = User.objects.create(
            username='doctor1',
            email='doc@clinica.com',
            password=make_password('password'),
            is_staff=False, 
            is_superuser=False,
            first_name="Gregory",
            last_name="Doe"
        )
        doctor.groups.add(grupo_medicos)

    # 3. Crear un Paciente de prueba (necesitamos un usuario admin para asignarlo)
    admin_user = User.objects.filter(username='admin').first()
    if admin_user and not Paciente.objects.filter(nombre='Juanito').exists():
        Paciente.objects.create(
            nombre='Jhon',
            apellido='Doe',
            fecha_nacimiento='1990-05-15',
            direccion='Calle Falsa 123',
            telefono='555-1234',
            email='juanito@gmail.com',
            creado_por=admin_user
        )

class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0002_auto_20251124_2207'), # Asegúrate que coincida con tu migración anterior
    ]

    operations = [
        migrations.RunPython(crear_datos_iniciales),
    ]