from django.urls import path
from . import views

# IMPORTANTE: Al tener app_name, tus URLs se llaman 'curriculum:nombre'
app_name = 'curriculum'

urlpatterns = [
    # HOME
    path('', views.home, name='home'),
    
    # PANEL PRINCIPAL
    path('panel/', views.panel_gestion, name='dashboard'),
    
    # AUTH
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # DATOS PERSONALES (Corregido a guion bajo para que coincida con tus views)
    path('agregar-datos/', views.agregar_datos_personales, name='agregar_datos_personales'),
    path('editar-datos/', views.editar_datos_personales, name='editar_datos_personales'),
    path('eliminar-datos/', views.eliminar_datos_personales, name='eliminar_datos_personales'),
    
    # EXPERIENCIA
    path('agregar-experiencia/', views.agregar_experiencia, name='agregar_experiencia'),
    path('editar-experiencia/<int:pk>/', views.editar_experiencia, name='editar_experiencia'),
    path('eliminar-experiencia/<int:pk>/', views.eliminar_experiencia, name='eliminar_experiencia'),
    
    # CURSOS
    path('agregar-curso/', views.agregar_curso, name='agregar_curso'),
    path('editar-curso/<int:pk>/', views.editar_curso, name='editar_curso'),
    path('eliminar-curso/<int:pk>/', views.eliminar_curso, name='eliminar_curso'),
    
    # RECONOCIMIENTOS
    path('agregar-reconocimiento/', views.agregar_reconocimiento, name='agregar_reconocimiento'),
    path('editar-reconocimiento/<int:pk>/', views.editar_reconocimiento, name='editar_reconocimiento'),
    path('eliminar-reconocimiento/<int:pk>/', views.eliminar_reconocimiento, name='eliminar_reconocimiento'),
    
    # PRODUCTOS ACADÉMICOS
    path('agregar-producto-academico/', views.agregar_producto_academico, name='agregar_producto_academico'),
    path('editar-producto-academico/<int:pk>/', views.editar_producto_academico, name='editar_producto_academico'),
    path('eliminar-producto-academico/<int:pk>/', views.eliminar_producto_academico, name='eliminar_producto_academico'),
    
    # PRODUCTOS LABORALES
    path('agregar-producto-laboral/', views.agregar_producto_laboral, name='agregar_producto_laboral'),
    path('editar-producto-laboral/<int:pk>/', views.editar_producto_laboral, name='editar_producto_laboral'),
    path('eliminar-producto-laboral/<int:pk>/', views.eliminar_producto_laboral, name='eliminar_producto_laboral'),
    
    # VENTA GARAGE
    path('agregar-venta/', views.agregar_venta, name='agregar_venta'),
    path('editar-venta/<int:pk>/', views.editar_venta, name='editar_venta'),
    path('eliminar-venta/<int:pk>/', views.eliminar_venta, name='eliminar_venta'),

    # GENERAR PDF
    path('exportar-pdf/', views.exportar_pdf_completo, name='exportar_pdf_completo'),
]