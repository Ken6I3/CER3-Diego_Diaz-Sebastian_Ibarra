from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProponerTallerForm
from .models import Taller
from .permisos import Admin_o_JV
from rest_framework import viewsets
from .serializers import TallerSerializer

# Create your views here.

class TallerSetVista(viewsets.ModelViewSet):
    queryset = Taller.objects.all()
    serializer_class = TallerSerializer
    permission_classes = [Admin_o_JV]
    def get_queryset(self):
        return Taller.objects.all().order_by("id")

def inicio(request):
    en_junta = False

    talleres = Taller.objects.filter(estado__in=["Aceptado", "Pendiente"])

    if request.user.is_authenticated:
        en_junta = request.user.groups.filter(name='Junta de vecinos').exists()
    return render(request, 'core/inicio.html', {'en_junta': en_junta, 'talleres':talleres})


def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home') 
    else:      
        form = AuthenticationForm()
    return render(request, 'core/iniciar_sesion.html', {'form': form})



@login_required
@user_passes_test(lambda u: u.groups.filter(name='Junta de vecinos').exists())

def organizar_taller(request):
    if request.method == 'POST':
        form = ProponerTallerForm(request.POST)
        if form.is_valid():
            taller = form.save(commit=False)
            taller.estado = "Pendiente"  
            taller.usuario = request.user  
            taller.save()
            return redirect('home')
    else:
        form = ProponerTallerForm()

    return render(request, 'core/organizar_taller.html', {'form': form})
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Junta de vecinos').exists())
def historial_talleres(request):
    talleres = (
        Taller.objects
        .select_related("profesor", "lugar", "categoria")
        .order_by("-fecha")
    )

    return render(request, "core/historial.html", {"talleres": talleres})