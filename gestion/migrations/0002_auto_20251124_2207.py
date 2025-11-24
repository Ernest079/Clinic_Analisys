from django.db import migrations
from django.contrib.auth.hashers import make_password

def crear_admin_defecto(apps, schema_editor):
    # Obtenemos el modelo de Usuario dinámicamente
    User = apps.get_model('auth', 'User')
    
    # Solo lo creamos si no existe
    if not User.objects.filter(username='admin').exists():
        User.objects.create(
            username='admin',
            email='admin@clinica.com',
            password=make_password('12345678'), # Contraseña hasheada
            is_superuser=True,
            is_staff=True
        )

class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'), # Asegúrate que esto coincida con tu última migración
    ]

    operations = [
        migrations.RunPython(crear_admin_defecto),
    ]