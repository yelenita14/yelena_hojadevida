import requests
import base64
import io
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.template.loader import render_to_string
from weasyprint import HTML

from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    Reconocimientos,
    CursosRealizados,
    ProductosAcademicos,
    ProductosLaborales,
    VentaGarage
)

from .forms import (
    SeleccionSeccionesForm,
    DatosPersonalesForm,
    ExperienciaLaboralForm,
    ReconocimientosForm,
    CursosRealizadosForm,
    ProductosAcademicosForm,
    ProductosLaboralesForm,
    VentaGarageForm
)

# FRONT

def home(request):
    return mi_hoja_vida(request)

def mi_hoja_vida(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()

    if not perfil:
        return render(request, 'curriculum/mi_hoja_vida.html', {'perfil': None})

    return render(request, 'curriculum/mi_hoja_vida.html', {
        'perfil': perfil,
        'experiencias': ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True),
        'reconocimientos': Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True),
        'cursos': CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True),
        'productos_academicos': ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True),
        'productos_laborales': ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True),
        'ventas': VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True),
    })

# AUTH

def user_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('curriculum:dashboard') # CORREGIDO
    return render(request, 'curriculum/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('curriculum:home') # CORREGIDO

# PANEL

@login_required
def panel_gestion(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    if not perfil:
        return redirect('curriculum:agregar_datos_personales') # CORREGIDO

    form_secciones = SeleccionSeccionesForm(request.POST or None, instance=perfil)
    if request.method == 'POST' and form_secciones.is_valid():
        form_secciones.save()

    return render(request, 'curriculum/dashboard.html', {
        'perfil': perfil,
        'form_secciones': form_secciones,
        'experiencias': ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil),
        'reconocimientos': Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil),
        'cursos': CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil),
        'productos_academicos': ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil),
        'productos_laborales': ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil),
        'ventas': VentaGarage.objects.filter(idperfilconqueestaactivo=perfil),
    })

# DATOS PERSONALES

@login_required
def agregar_datos_personales(request):
    form = DatosPersonalesForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        perfil = form.save(commit=False)
        perfil.perfilactivo = 1
        perfil.save()
        return redirect('curriculum:dashboard') # CORREGIDO
    return render(request, 'curriculum/datos_personales.html', {'form': form})

@login_required
def editar_datos_personales(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    form = DatosPersonalesForm(request.POST or None, request.FILES or None, instance=perfil)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('curriculum:dashboard') # CORREGIDO
    return render(request, 'curriculum/datos_personales.html', {'form': form})

@login_required
def eliminar_datos_personales(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    if perfil:
        perfil.delete()
    return redirect('curriculum:dashboard')
# CRUD GENÉRICO

@login_required
def agregar_generico(request, Form, template):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    if not perfil:
        return redirect('curriculum:agregar_datos_personales') # CORREGIDO

    form = Form(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.idperfilconqueestaactivo = perfil
        obj.save()
        return redirect('curriculum:dashboard') # CORREGIDO
    return render(request, template, {'form': form})

@login_required
def editar_generico(request, Model, Form, template, pk):
    obj = get_object_or_404(Model, pk=pk)
    form = Form(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('curriculum:dashboard') # CORREGIDO
    return render(request, template, {'form': form})

@login_required
def eliminar_generico(request, Model, pk):
    obj = get_object_or_404(Model, pk=pk)
    obj.delete()
    return redirect('curriculum:dashboard') # CORREGIDO

# CRUD ESPECÍFICOS

@login_required
def agregar_experiencia(request):
    return agregar_generico(request, ExperienciaLaboralForm, 'curriculum/experiencia_form.html')

@login_required
def editar_experiencia(request, pk):
    return editar_generico(request, ExperienciaLaboral, ExperienciaLaboralForm, 'curriculum/experiencia_form.html', pk)

@login_required
def eliminar_experiencia(request, pk):
    return eliminar_generico(request, ExperienciaLaboral, pk)

@login_required
def agregar_curso(request):
    return agregar_generico(request, CursosRealizadosForm, 'curriculum/cursos_form.html')

@login_required
def editar_curso(request, pk):
    return editar_generico(request, CursosRealizados, CursosRealizadosForm, 'curriculum/cursos_form.html', pk)

@login_required
def eliminar_curso(request, pk):
    return eliminar_generico(request, CursosRealizados, pk)

@login_required
def agregar_reconocimiento(request):
    return agregar_generico(request, ReconocimientosForm, 'curriculum/reconocimientos_form.html')

@login_required
def editar_reconocimiento(request, pk):
    return editar_generico(request, Reconocimientos, ReconocimientosForm, 'curriculum/reconocimientos_form.html', pk)

@login_required
def eliminar_reconocimiento(request, pk):
    return eliminar_generico(request, Reconocimientos, pk)

@login_required
def agregar_producto_academico(request):
    return agregar_generico(request, ProductosAcademicosForm, 'curriculum/productos_academicos_form.html')

@login_required
def editar_producto_academico(request, pk):
    return editar_generico(request, ProductosAcademicos, ProductosAcademicosForm, 'curriculum/productos_academicos_form.html', pk)

@login_required
def eliminar_producto_academico(request, pk):
    return eliminar_generico(request, ProductosAcademicos, pk)

@login_required
def agregar_producto_laboral(request):
    return agregar_generico(request, ProductosLaboralesForm, 'curriculum/productos_laborales_form.html')

@login_required
def editar_producto_laboral(request, pk):
    return editar_generico(request, ProductosLaborales, ProductosLaboralesForm, 'curriculum/productos_laborales_form.html', pk)

@login_required
def eliminar_producto_laboral(request, pk):
    return eliminar_generico(request, ProductosLaborales, pk)

@login_required
def agregar_venta(request):
    return agregar_generico(request, VentaGarageForm, 'curriculum/venta_garage_form.html')

@login_required
def editar_venta(request, pk):
    return editar_generico(request, VentaGarage, VentaGarageForm, 'curriculum/venta_garage_form.html', pk)

@login_required
def eliminar_venta(request, pk):
    return eliminar_generico(request, VentaGarage, pk)

# PDF
def exportar_pdf_completo(request):
    datos = DatosPersonales.objects.filter(perfilactivo=1).first()
    if not datos:
        return HttpResponse("No hay perfil activo", status=404)
    
    filtros = {'idperfilconqueestaactivo': datos, 'activarparaqueseveaenfront': True}

    def get_base64(url):
        """Descarga una imagen y la pasa a base64 para el PDF"""
        if not url: return None
        try:
            r = requests.get(url, timeout=10)
            return base64.b64encode(r.content).decode()
        except: return None

    context = {
        'datos': datos,
        'foto_base64': get_base64(datos.foto_perfil.url) if datos.foto_perfil else None,
    }

    # SECCIONES (Solo texto, excepto Venta Garage)
    if request.GET.get('exp') == 'on':
        context['experiencias'] = [{'empresa': e.nombrempresa, 'cargo': e.cargodesempenado} for e in ExperienciaLaboral.objects.filter(**filtros)]

    if request.GET.get('cursos') == 'on':
        context['cursos'] = [{'nombre': c.nombrecurso, 'entidad': c.entidadpatrocinadora} for c in CursosRealizados.objects.filter(**filtros)]

    if request.GET.get('logros') == 'on':
        context['reconocimientos'] = [{'nombre': getattr(r, 'tiporeconocimiento', 'Logro'), 'entidad': r.entidadpatrocinadora} for r in Reconocimientos.objects.filter(**filtros)]

    if request.GET.get('prod_acad') == 'on':
        context['productos_academicos'] = [{'nombre': pa.nombrerecurso} for pa in ProductosAcademicos.objects.filter(**filtros)]

    if request.GET.get('proyectos') == 'on':
        context['productos_laborales'] = [{'nombre': pl.nombreproducto} for pl in ProductosLaborales.objects.filter(**filtros)]

    # VENTA GARAGE (Mantiene la imagen)
    if request.GET.get('venta') == 'on':
        context['ventas'] = [{
            'nombre': v.nombreproducto,
            'precio': v.valordelbien,
            'estado': v.estadoproducto,
            'foto_64': get_base64(v.imagen_producto.url) if v.imagen_producto else None
        } for v in VentaGarage.objects.filter(idperfilconqueestaactivo=datos)]

    html_string = render_to_string('curriculum/pdf.html', context)
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="HV_{datos.apellidos}.pdf"'
    return response