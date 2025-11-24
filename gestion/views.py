from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Paciente, Diagnostico, Enfermedad
from django.contrib.auth.models import User

# 1. Vista del Dashboard (Protegida con login)
@login_required
def dashboard_view(request):
    # Recopilamos datos para mostrar métricas
    total_pacientes = Paciente.objects.count()
    total_diagnosticos = Diagnostico.objects.count()
    # Últimos 5 diagnósticos
    ultimos_diagnosticos = Diagnostico.objects.select_related('paciente', 'enfermedad_diagnosticada').order_by('-fecha_diagnostico')[:5]

    context = {
        'total_pacientes': total_pacientes,
        'total_diagnosticos': total_diagnosticos,
        'ultimos_diagnosticos': ultimos_diagnosticos
    }
    return render(request, 'gestion/dashboard.html', context)


@login_required
def lista_medicos(request):
    # Filtramos usuarios que pertenecen al grupo 'Medicos'
    medicos = User.objects.filter(groups__name='Medicos')
    return render(request, 'gestion/lista_usuarios.html', {
        'usuarios': medicos, 
        'titulo': 'Gestión de Médicos',
        'rol': 'Médico'
    })

# LISTA DE PACIENTES (Tu modelo Paciente)
@login_required
def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    # Usaremos una plantilla diferente porque los campos son distintos
    return render(request, 'gestion/lista_pacientes.html', {'pacientes': pacientes})

# LISTA DE ADMINS (Solo accesible por superusuarios)
@login_required
def lista_admins(request):
    if not request.user.is_superuser:
        return redirect('dashboard') # Protección simple
        
    admins = User.objects.filter(is_superuser=True)
    return render(request, 'gestion/lista_usuarios.html', {
        'usuarios': admins, 
        'titulo': 'Gestión de Administradores',
        'rol': 'Admin'
    })