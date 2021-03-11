from django.db import models
from django.urls import reverse


class Empresa(models.Model):
    nome = models.CharField(max_length=100, help_text='Nome da empresas')

    def __str__(self):
        return self.nome

    # METODO PARA REDIRECIONAMENTO APOS CONCLUSÃO DE EDIÇÃO OU SALVAMENTO DO FORMULARIO
    def get_absolute_url(self):
        return reverse('home')

