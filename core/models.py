from django.db import models

# Create your models here.

class Seller(models.Model):
    horario = models.CharField(max_length=255)
    contacto = models.IntegerField(blank=True, null=True)
    instagram = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name