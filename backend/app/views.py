from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, CreateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
import requests
import base64
from app.models import Auditoria

# Create your views here.
def error404(request, exception):
    return render(request, '404.html')

class AuditoriaView(LoginRequiredMixin, View):
    template_name = "cargar.html"

    def get(self, request):
        return render(request, self.template_name)

class EnviarPDF(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request):
        archivo = {
            "archivo": request.FILES["archivo"]
        }

        archivo_leido = requests.post('http://ai-engine:8000/api/', files=archivo, timeout=10)
        texto_limpio = archivo_leido.json().get("contenido", "")
        texto_limpio = texto_limpio.replace(".\n", ".[[PARRAFO]]")
        texto_limpio = texto_limpio.replace(". \n", ".[[PARRAFO]]")
        texto_limpio = texto_limpio.replace("\r\n", "[[PARRAFO]]")
        texto_limpio = texto_limpio.replace("\n\n", "[[PARRAFO]]")
        texto_limpio = texto_limpio.replace(r"\.\s*\n", ".[[PARRAFO]]")
        texto_limpio = texto_limpio.replace(" \n ", "[[PARRAFO]]")
        texto_limpio = texto_limpio.replace("\n", "")
        texto_limpio = texto_limpio.replace("[[PARRAFO]]", "\n\n")

        archivo_pdf = request.FILES["archivo"]
        
        datos = {
            "tipo": request.POST.get("tipo"),
            "archivo": texto_limpio
        }
        respuesta = requests.post('http://ai-engine:8000/api/ia', json=datos)
        respuesta_json = respuesta.json()

        if respuesta_json.get("Error"):
            archivo_raw = request.FILES.get("archivo")
            archivo_raw.seek(0)
            archivo_binario = archivo_raw.read()
            pdf_base64 = base64.b64encode(archivo_binario).decode("utf-8")
            
            auditoria = {"archivo": pdf_base64}
        else:
            auditoria = Auditoria.objects.create(
                puntos_clave=respuesta_json.get("puntos_clave", [0]),
                banderas_rojas=respuesta_json.get("banderas_rojas", []),
                riesgo_total=respuesta_json.get("riesgo_total", "No analizado"),
                tipo=datos["tipo"],
                archivo=archivo_pdf,
                nombre_archivo=archivo_pdf.name,
                creador=request.user,
                cliente=request.POST.get("cliente")
            )

        mostrar_datos = [datos, auditoria, respuesta_json]
        
        return render(request, 'auditoria.html', {"respuesta": mostrar_datos})

class DashboardView(LoginRequiredMixin, View):
    template_name = 'listado.html'

    def get(self, request):
        auditorias = Auditoria.objects.filter(creador=request.user).order_by("fecha")
        return render(request, self.template_name, {"auditorias": auditorias})

class AnonymousMixin(UserPassesTestMixin):
    # Clase que verifica que el usuario no ha iniciado sesión
    def test_func(self):
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return redirect('/tasks/')

class LoginView(AnonymousMixin, auth_views.LoginView):
    template_name = 'registration/login.html'

class RegisterView(AnonymousMixin, CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/login/'
