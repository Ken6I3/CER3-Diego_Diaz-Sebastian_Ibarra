from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProponerTallerForm
from .models import Taller
import requests

from rest_framework import viewsets
from .serializers import TallerSerializer

# Create your views here.

class TallerSetVista(viewsets.ModelViewSet):
    queryset = Taller.objects.all()
    serializer_class = TallerSerializer

def inicio(request):
    en_junta = False

    url = "https://api.boostr.cl/holidays.json"

    response = requests.get(url)

    if response.status_code == 200:
        datos = response.json()
        feriados = datos.get('data',[])
    else:
        feriados = []

    talleres = Taller.objects.all()

    if request.user.is_authenticated:
        en_junta = request.user.groups.filter(name='Junta de vecinos').exists()
    return render(request, 'core/inicio.html', {'en_junta': en_junta,'feriados':feriados, 'talleres':talleres})


def iniciar_sesion(request):
    # En caso de que sea POST, es decir cuando el usuario envía los datos, se crea una forma para que el servidor HTTP lo lea
    if request.method == 'POST':
        # Se crea el form donde se guardarán los datos que el usuario envió
        form = AuthenticationForm(request, data=request.POST)
        # Se verifica si los datos son validos, si existen dentro de la base de datos o no
        if form.is_valid():
            # En caso de ser válido se inicia, utiliza el form.get_user() para obtener el usuario y logearlo
            user = form.get_user()
            login(request, user)
            return redirect('home') 
    else:
       # En caso de que el metodo no sea POST, sino que sea GET (cargar la pagina), se hace este else
        # En el que se crea el formulario para que el usuario lo pueda llenar y posteriormente enviarlo        
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
    

