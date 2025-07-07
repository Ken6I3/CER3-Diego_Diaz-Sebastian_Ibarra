from django.contrib import admin
from .models import Taller, Lugar, Profesor, Categoria
# Register your models here.

admin.site.register(Taller)
admin.site.register(Lugar)
admin.site.register(Profesor)
admin.site.register(Categoria)

