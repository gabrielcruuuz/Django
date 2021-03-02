from django.db import models
from django.contrib.auth.models import User

from apps.departamentos.models import Departamento
from apps.empresas.models import Empresa


class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    # CASCADE ON DELETE ao remover esse objeto funcionario, ele ira remover o usuario automaticamente
    # USANDO O PROTECT, PRIMEIRO VC DELETA O FUNCIONARIO E SE FOR O CASO DEPOIS O USUARIO
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    lista_departamentos = models.ManyToManyField(Departamento)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.nome
