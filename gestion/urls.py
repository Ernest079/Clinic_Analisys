from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Vista de Login nativa de Django
    path('', auth_views.LoginView.as_view(template_name='gestion/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Nuestro Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('medicos/', views.lista_medicos, name='lista_medicos'),
    path('medicos/nuevo/', views.crear_medico, name='crear_medico'),

    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('pacientes/nuevo/', views.crear_paciente, name='crear_paciente'),
    
    path('administradores/', views.lista_admins, name='lista_admins'),
    path('administradores/nuevo/', views.crear_admin, name='crear_admin'),

    path('enfermedades/', views.lista_enfermedades, name='lista_enfermedades'),
    path('enfermedades/nueva/', views.crear_enfermedad, name='crear_enfermedad'),
    path('enfermedades/editar/<int:id>/', views.editar_enfermedad, name='editar_enfermedad'),
    path('enfermedades/eliminar/<int:id>/', views.eliminar_enfermedad, name='eliminar_enfermedad'),

    path('sintomas/', views.lista_sintomas, name='lista_sintomas'),
    path('sintomas/nuevo/', views.crear_sintoma, name='crear_sintoma'),
    path('sintomas/editar/<int:id>/', views.editar_sintoma, name='editar_sintoma'),
    path('sintomas/eliminar/<int:id>/', views.eliminar_sintoma, name='eliminar_sintoma'),

    path('signos/', views.lista_signos, name='lista_signos'),
    path('signos/nuevo/', views.crear_signo, name='crear_signo'),
    path('signos/editar/<int:id>/', views.editar_signo, name='editar_signo'),
    path('signos/eliminar/<int:id>/', views.eliminar_signo, name='eliminar_signo'),

    path('diagnosticos/', views.lista_diagnosticos, name='lista_diagnosticos'),
    path('diagnosticos/nuevo/', views.crear_diagnostico, name='crear_diagnostico'),
    path('diagnosticos/editar/<int:id>/', views.editar_diagnostico, name='editar_diagnostico'),
    path('diagnosticos/eliminar/<int:id>/', views.eliminar_diagnostico, name='eliminar_diagnostico'),

    path('inferencia/', views.motor_inferencia, name='motor_inferencia'),
]