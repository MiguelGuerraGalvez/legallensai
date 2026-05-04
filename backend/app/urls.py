from django.urls import path
from app.views import AuditoriaView, EnviarPDF, DashboardView, LoginView, RegisterView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', DashboardView.as_view(), name='listado'),
    path('cargar/', AuditoriaView.as_view(), name='cargar'),
    path('respuesta/', EnviarPDF.as_view(), name='respuesta'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
