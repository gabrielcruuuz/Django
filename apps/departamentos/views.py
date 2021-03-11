from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from .models import Departamento
# Create your views here.
from ..funcionarios.models import Funcionario


class DepartamentoList(ListView):
    model = Departamento

    def get_queryset(self):
        funcionario_logado = Funcionario.objects.get(user=self.request.user)
        empresa_funcionaro_logado = funcionario_logado.empresa
        queryset = Departamento.objects.filter(empresa=empresa_funcionaro_logado)

        return queryset


class DepartamentoCreate(CreateView):
    model = Departamento
    fields = ['nome']

    def form_valid(self, form):
        # cria o objeto mas ainda não salva no banco
        departamento_novo = form.save(commit=False)

        empresa_usuario_logado = Funcionario.objects.filter(user=self.request.user)[0].empresa
        departamento_novo.empresa = empresa_usuario_logado

        departamento_novo.save()

        return super(DepartamentoCreate, self).form_valid(form)


class DepartamentoEdit(UpdateView):
    model = Departamento
    fields = ['nome']


class DepartamentoDelete(DeleteView):
    model = Departamento
    success_url = reverse_lazy('list_departamentos')

