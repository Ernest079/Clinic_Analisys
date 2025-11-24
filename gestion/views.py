from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Paciente, Diagnostico, Enfermedad
from django.contrib.auth.models import User
from .forms import PacienteForm, RegistroUsuarioForm
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import EnfermedadForm
from django.shortcuts import get_object_or_404


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


@login_required
def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.creado_por = request.user # Asignamos quien lo creó
            paciente.save()
            messages.success(request, 'Paciente registrado correctamente.')
            return redirect('lista_pacientes')
    else:
        form = PacienteForm()
    
    return render(request, 'gestion/formulario.html', {
        'form': form, 
        'titulo': 'Registrar Nuevo Paciente',
        'boton': 'Guardar Paciente'
    })

# 2. CREAR MÉDICO
@login_required
def crear_medico(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) # Encriptamos contraseña
            user.save()
            
            # Asignar grupo Médicos
            grupo_medicos = Group.objects.get(name='Medicos')
            user.groups.add(grupo_medicos)
            
            messages.success(request, 'Médico registrado exitosamente.')
            return redirect('lista_medicos')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'gestion/formulario.html', {
        'form': form, 
        'titulo': 'Registrar Nuevo Médico',
        'boton': 'Guardar Médico'
    })

# 3. CREAR ADMINISTRADOR
@login_required
def crear_admin(request):
    if not request.user.is_superuser: # Solo un superuser puede crear otros admins
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_staff = True
            user.is_superuser = True
            user.save()
            
            messages.success(request, 'Administrador registrado exitosamente.')
            return redirect('lista_admins')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'gestion/formulario.html', {
        'form': form, 
        'titulo': 'Registrar Nuevo Administrador',
        'boton': 'Guardar Admin'
    })

# |-----------------------CRUD ENFERMEDADES-----------------------|

@login_required
def lista_enfermedades(request):
    enfermedades = Enfermedad.objects.all().order_by('nombre')
    return render(request, 'gestion/lista_enfermedades.html', {'enfermedades': enfermedades})

# 2. CREAR (CREATE)
@login_required
def crear_enfermedad(request):
    if request.method == 'POST':
        form = EnfermedadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enfermedad registrada correctamente.')
            return redirect('lista_enfermedades')
    else:
        form = EnfermedadForm()
    
    return render(request, 'gestion/formulario.html', {
        'form': form, 
        'titulo': 'Registrar Nueva Enfermedad', 
        'boton': 'Guardar Enfermedad'
    })

# 3. EDITAR (UPDATE)
@login_required
def editar_enfermedad(request, id):
    enfermedad = get_object_or_404(Enfermedad, id=id)
    if request.method == 'POST':
        form = EnfermedadForm(request.POST, instance=enfermedad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enfermedad actualizada.')
            return redirect('lista_enfermedades')
    else:
        form = EnfermedadForm(instance=enfermedad)

    return render(request, 'gestion/formulario.html', {
        'form': form, 
        'titulo': f'Editar {enfermedad.nombre}', 
        'boton': 'Actualizar'
    })

# 4. ELIMINAR (DELETE)
@login_required
def eliminar_enfermedad(request, id):
    enfermedad = get_object_or_404(Enfermedad, id=id)
    enfermedad.delete()
    messages.success(request, 'Enfermedad eliminada.')
    return redirect('lista_enfermedades') 