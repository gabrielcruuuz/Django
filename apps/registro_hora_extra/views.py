from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from .forms import RegistroHoraExtraForm
from .models import RegistroHoraExtra
from ..funcionarios.models import Funcionario


class HoraExtraList(ListView):
    model = RegistroHoraExtra

    def get_queryset(self):
        funcionario_logado = Funcionario.objects.get(user=self.request.user)
        empresa_funcionaro_logado = funcionario_logado.empresa
        queryset = RegistroHoraExtra.objects.filter(funcionario__empresa=empresa_funcionaro_logado)

        return queryset


class HoraExtraEdit(UpdateView):
    model = RegistroHoraExtra
    fields = ['motivo', 'horas']


class HoraExtraDelete(DeleteView):
    model = RegistroHoraExtra
    success_url = reverse_lazy('list_hora_extra')


class HoraExtraCreate(CreateView):
    model = RegistroHoraExtra
    # ALTERANDO O FORM PADRÃO PARA UM FORM CUSTOMIZADO
    form_class = RegistroHoraExtraForm

    def get_form_kwargs(self):
        # TRANSFORMANDO A VARIAVEL USER (QUEM FEZ A REQUISIÇÃO) EM UM PARAMETRO A SER USADO NO FORM CUSTOMIZADO
        kwargs = super(HoraExtraCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

