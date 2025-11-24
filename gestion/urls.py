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
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('administradores/', views.lista_admins, name='lista_admins'),
]