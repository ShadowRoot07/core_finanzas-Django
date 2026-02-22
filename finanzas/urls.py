from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('exportar-csv/', views.exportar_csv, name='exportar_csv'),
    path('descargar-pdf/', views.descargar_reporte_pdf, name='descargar_reporte_pdf'),
]

