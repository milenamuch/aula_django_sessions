from django.db import models
from django.contrib.auth.models import User

class EnderecoUsuario(models.Model):
    
    rua = models.CharField(max_length=100, blank=True, null=True)
    numero = models.CharField(max_length=6, blank=True, null=True)
    cep = models.CharField(max_length=8, blank=True, null=True)
    usuario = models.ForeignKey (User, on_delete=models.DO_NOTHING)
    
    def __str__(self) -> str:
        return self.usuario.username