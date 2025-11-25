from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Paciente, Diagnostico, Enfermedad, Sintoma, Signo
from django.contrib.auth.models import User
from .forms import PacienteForm, RegistroUsuarioForm
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import EnfermedadForm, SintomaForm, SignoForm, DiagnosticoForm, InferenciaForm
from django.shortcuts import get_object_or_404
from django.db.models import Count

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

# |-----------------------------CRUD DIAGNOSTICOS----------------------------------|

# ==========================================
# 1. CRUD SÍNTOMAS
# ==========================================
@login_required
def lista_sintomas(request):
    sintomas = Sintoma.objects.all().order_by('nombre')
    return render(request, 'gestion/lista_sintomas.html', {'items': sintomas, 'tipo': 'Síntoma'})

@login_required
def crear_sintoma(request):
    if request.method == 'POST':
        form = SintomaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Síntoma agregado.')
            return redirect('lista_sintomas')
    else:
        form = SintomaForm()
    return render(request, 'gestion/formulario.html', {'form': form, 'titulo': 'Nuevo Síntoma', 'boton': 'Guardar'})

@login_required
def editar_sintoma(request, id):
    obj = get_object_or_404(Sintoma, id=id)
    if request.method == 'POST':
        form = SintomaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('lista_sintomas')
    else:
        form = SintomaForm(instance=obj)
    return render(request, 'gestion/formulario.html', {'form': form, 'titulo': 'Editar Síntoma', 'boton': 'Actualizar'})

@login_required
def eliminar_sintoma(request, id):
    obj = get_object_or_404(Sintoma, id=id)
    obj.delete()
    return redirect('lista_sintomas')

# ==========================================
# 2. CRUD SIGNOS
# ==========================================
@login_required
def lista_signos(request):
    signos = Signo.objects.all().order_by('nombre')
    return render(request, 'gestion/lista_signos.html', {'items': signos, 'tipo': 'Signo'})

@login_required
def crear_signo(request):
    if request.method == 'POST':
        form = SignoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Signo agregado.')
            return redirect('lista_signos')
    else:
        form = SignoForm()
    return render(request, 'gestion/formulario.html', {'form': form, 'titulo': 'Nuevo Signo', 'boton': 'Guardar'})

@login_required
def editar_signo(request, id):
    obj = get_object_or_404(Signo, id=id)
    if request.method == 'POST':
        form = SignoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('lista_signos')
    else:
        form = SignoForm(instance=obj)
    return render(request, 'gestion/formulario.html', {'form': form, 'titulo': 'Editar Signo', 'boton': 'Actualizar'})

@login_required
def eliminar_signo(request, id):
    obj = get_object_or_404(Signo, id=id)
    obj.delete()
    return redirect('lista_signos')

# ==========================================
# 3. CRUD DIAGNÓSTICOS (El más importante)
# ==========================================
@login_required
def lista_diagnosticos(request):
    # Optimizamos la consulta con select_related para traer datos del paciente y medico en una sola query
    diagnosticos = Diagnostico.objects.select_related('paciente', 'medico', 'enfermedad_diagnosticada').all().order_by('-fecha_diagnostico')
    return render(request, 'gestion/lista_diagnosticos.html', {'diagnosticos': diagnosticos})

@login_required
def crear_diagnostico(request):
    if request.method == 'POST':
        form = DiagnosticoForm(request.POST)
        if form.is_valid():
            diagnostico = form.save(commit=False)
            diagnostico.medico = request.user  # ASIGNACIÓN AUTOMÁTICA DEL MÉDICO
            diagnostico.save()
            form.save_m2m() # Importante cuando hay ManyToMany en commit=False
            messages.success(request, 'Diagnóstico registrado exitosamente.')
            return redirect('lista_diagnosticos')
    else:
        form = DiagnosticoForm()
    
    return render(request, 'gestion/formulario.html', {'form': form, 'titulo': 'Realizar Diagnóstico', 'boton': 'Guardar Diagnóstico'})

@login_required
def editar_diagnostico(request, id):
    diagnostico = get_object_or_404(Diagnostico, id=id)
    # Opcional: Validar que solo el médico que lo creó pueda editarlo
    # if diagnostico.medico != request.user: return redirect('dashboard')

    if request.method == 'POST':
        form = DiagnosticoForm(request.POST, instance=diagnostico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Diagnóstico actualizado.')
            return redirect('lista_diagnosticos')
    else:
        form = DiagnosticoForm(instance=diagnostico)
    return render(request, 'gestion/formulario.html', {'form': form, 'titulo': 'Editar Diagnóstico', 'boton': 'Actualizar'})

@login_required
def eliminar_diagnostico(request, id):
    diagnostico = get_object_or_404(Diagnostico, id=id)
    diagnostico.delete()
    messages.success(request, 'Diagnóstico eliminado.')
    return redirect('lista_diagnosticos')

# ==========================================
# 1. MOTOR DE INFERENCIA
# ==========================================
@login_required
def motor_inferencia(request):
    resultado = None
    diagnostico_sugerido = []

    if request.method == 'POST':
        form = InferenciaForm(request.POST)
        if form.is_valid():
            # 1. Obtenemos los datos que ingresó el médico
            sintomas_input = form.cleaned_data['sintomas']
            signos_input = form.cleaned_data['signos']
            
            # Convertimos a sets (conjuntos) para hacer operaciones matemáticas rápidas
            ids_sintomas_input = set(s.id for s in sintomas_input)
            ids_signos_input = set(s.id for s in signos_input)
            
            todas_enfermedades = Enfermedad.objects.prefetch_related('sintomas', 'signos')

            ranking = []

            # 2. EL ALGORITMO DE PREDICCIÓN
            for enfermedad in todas_enfermedades:
                # Obtenemos los IDs de los síntomas/signos reales de la enfermedad
                ids_sintomas_reales = set(s.id for s in enfermedad.sintomas.all())
                ids_signos_reales = set(s.id for s in enfermedad.signos.all())

                # Unión de características de la enfermedad (El total de puntos posibles)
                total_caracteristicas_enfermedad = len(ids_sintomas_reales) + len(ids_signos_reales)

                if total_caracteristicas_enfermedad > 0:
                    # Intersección: ¿Cuántos coinciden?
                    coincidencias_sintomas = len(ids_sintomas_input.intersection(ids_sintomas_reales))
                    coincidencias_signos = len(ids_signos_input.intersection(ids_signos_reales))
                    
                    total_coincidencias = coincidencias_sintomas + coincidencias_signos

                    # Cálculo de Probabilidad (Simple Ratio)
                    # Fórmula: (Coincidencias / Total de la Enfermedad) * 100
                    porcentaje = (total_coincidencias / total_caracteristicas_enfermedad) * 100
                    
                    # Solo agregamos si hay alguna coincidencia relevante (>0%)
                    if porcentaje > 0:
                        ranking.append({
                            'enfermedad': enfermedad,
                            'porcentaje': round(porcentaje, 1),
                            'coincidencias': total_coincidencias,
                            'total_items': total_caracteristicas_enfermedad
                        })

            # 3. Ordenamos de mayor a menor probabilidad
            diagnostico_sugerido = sorted(ranking, key=lambda x: x['porcentaje'], reverse=True)
            resultado = True

    else:
        form = InferenciaForm()

    return render(request, 'gestion/motor_inferencia.html', {
        'form': form,
        'resultado': resultado,
        'diagnostico_sugerido': diagnostico_sugerido
    })