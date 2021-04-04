from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

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

    # METODO PARA REDIRECIONAMENTO APOS CONCLUSÃO DE EDIÇÃO OU SALVAMENTO DO FORMULARIO

    def get_absolute_url(self):
        return reverse('list_funcionarios')

    # CRIANDO VARIAVEL PRA USAR NO TEMPLATE
    @property
    def total_hora_extra(self):
        # Somando os valores das horas (tipo um =+ ) direto da lista
        total = self.registrohoraextra_set.filter(utilizada=False).aggregate(Sum('horas'))['horas__sum']

        # IF TOTAL == NONEH RETORNA 0
        return total or 0


