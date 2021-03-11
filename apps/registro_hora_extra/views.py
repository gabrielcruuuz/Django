from django.shortcuts import render
from django.views.generic import ListView

from .models import RegistroHoraExtra
from ..funcionarios.models import Funcionario


class HoraExtraList(ListView):
    model = RegistroHoraExtra

    def get_queryset(self):
        funcionario_logado = Funcionario.objects.get(user=self.request.user)
        empresa_funcionaro_logado = funcionario_logado.empresa
        queryset = RegistroHoraExtra.objects.filter(funcionario__empresa=empresa_funcionaro_logado)

        return queryset


