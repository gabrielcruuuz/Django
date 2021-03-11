from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView

from apps.documentos.models import Documento
from apps.funcionarios.models import Funcionario


class DocumentoCreate(CreateView):
    model = Documento
    fields = ['descricao', 'arquivo']

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.funcionario_id = self.kwargs['funcionario_id']

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

        # def get_success_url(self):
        #     return reverse('update_funcionarios', args=[self.kwargs['funcionario_id']])


class DocumentoDelete(DeleteView):
    model = Documento
    success_url = reverse_lazy('list_funcionarios')



