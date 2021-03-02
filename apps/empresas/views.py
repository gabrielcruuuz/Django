from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView

from .models import Empresa
from apps.funcionarios.models import Funcionario


class EmpresaCreate(CreateView):
    model = Empresa
    fields = ['nome']

    def form_valid(self, form):
        # RESGATANDO O OBJECTO DO BIND DO FORMULARIO
        obj = form.save();
        funcionario = Funcionario.objects.get(user=self.request.user)

        funcionario.empresa = obj
        funcionario.save()

        return HttpResponse('OK')

