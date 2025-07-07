"""
URL configuration for Certamen3_TLP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views
from django.contrib.auth.views import LogoutView

router = DefaultRouter()
router.register("talleres",views.TallerSetVista)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name="home"),
    path('iniciar_sesion/', views.iniciar_sesion, name="iniciar_sesion"),
    path('cerrar_sesion/', LogoutView.as_view(next_page='home'), name='Cerrar_sesion'),
    path('organizar_taller/', views.organizar_taller, name="organizar_taller"),
    path('historial_talleres/', views.historial_talleres, name="historial_talleres"),
    path('api/',include(router.urls)),
]
