from django.db import models

# Create your models here.
class profile (models.Model):
    name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    age = models.IntegerField()
    status =models.BooleanField(default=True)

# Comentario subir 