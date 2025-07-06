from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User, Group
from .models import Taller



class CustomUserAdmin(DefaultUserAdmin):
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        usuario = form.instance
        funcionario = Group.objects.filter(name="Funcionario municipal").first()

        if funcionario and funcionario in usuario.groups.all() and not usuario.is_staff:
            usuario.is_staff = True
            usuario.save(update_fields=["is_staff"])
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Taller)