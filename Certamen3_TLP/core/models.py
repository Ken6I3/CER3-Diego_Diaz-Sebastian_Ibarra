from django.db import models

CATEGORIAS = [
    ("1", "Aire Libre"),
    ("2", "Arte"),
    ("3", "Música"),
    ("4", "Salud"),
    ("5", "Tecnología"),
    ("6", "Oficios"),
    ("7", "Educación"),
    ("8", "Medioambiente"),
    ("9", "Comunidad y Liderazgo"),
    ("10", "Recreación"),
]

LUGARES = [
    ("1", "Jardín Botánico"),
    ("2", "Playa El Encanto"),
    ("3", "Biblioteca Municipal"),
    ("4", "Centro Cultural Villa Verde"),
    ("5", "Gimnasio Municipal"),
    ("6", "Sede Junta Vecinal N°5"),
    ("7", "Sede Junta Vecinal N°12"),
    ("8", "Parque Comunal"),
    ("9", "Salón Multiuso Municipal"),
    ("10", "Escuela Básica Villa Verde"),
]

ESTADO = [
    ("Pendiente", "Pendiente"),
    ("Aceptado", "Aceptado"),
    ("Rechazado", "Rechazado"),
]

class Taller(models.Model):
    fecha = models.DateField()
    duracion_horas = models.PositiveSmallIntegerField(help_text="Duración en horas")
    profesor = models.CharField(max_length=100)
    estado = models.CharField(max_length=12, choices=ESTADO, default="Pendiente")
    lugar = models.CharField(max_length=2, choices=LUGARES)       
    categoria = models.CharField(max_length=2, choices=CATEGORIAS) 

    class Meta:
        ordering = ["fecha", "lugar"]
        verbose_name = "Taller"
        verbose_name_plural = "Talleres"

    def __str__(self):
        return f"{self.get_categoria_display()} • {self.fecha:%d/%m/%Y} • {self.profesor}"
