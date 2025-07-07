from django.db import models
import requests

class Profesor(models.Model):
    nombre_completo = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_completo


class Lugar(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre + " - " + self.direccion


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre + " - " + self.descripcion


ESTADO = [
    ("Pendiente", "Pendiente"),
    ("Aceptado", "Aceptado"),
    ("Rechazado", "Rechazado"),
]

class Taller(models.Model):
    nombre = models.CharField(max_length=150)
    fecha = models.DateField()
    duracion = models.PositiveSmallIntegerField(help_text="Duración en horas")
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    estado = models.CharField(max_length=12, choices=ESTADO, default="Pendiente")
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)   
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    observacion = models.TextField(blank=True, null=True)
    def save(self, *args, **kwargs):
        url = "https://api.boostr.cl/holidays.json"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                feriados = response.json().get("data", [])
                for f in feriados:
                    if f["date"] == self.fecha.strftime("%Y-%m-%d"):
                        if f.get("inalienable", False):
                            self.estado = "Rechazado"
                            self.observacion = "No se programan talleres en feriados irrenunciables."
                        else:
                            if self.categoria.nombre != "Aire Libre":
                                self.estado = "Rechazado"
                                self.observacion = "Solo se permiten talleres de Aire Libre en feriados renunciables."
            else:
                print("No se pudo consultar la API de feriados")
        except Exception as e:
            print(f"Error al consultar la API: {e}")

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["fecha", "lugar"]
        verbose_name = "Taller"
        verbose_name_plural = "Talleres"

    def __str__(self):
        return f"{self.nombre} - {self.get_categoria_display()} - {self.fecha:%d/%m/%Y} - {self.profesor}"
