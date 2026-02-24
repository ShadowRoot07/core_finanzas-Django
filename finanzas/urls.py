from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='finanzas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('exportar-csv/', views.exportar_csv, name='exportar_csv'),
    path('descargar-pdf/', views.descargar_reporte_pdf, name='descargar_reporte_pdf'),
]

