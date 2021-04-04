import json
import xlwt

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
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


class HoraExtraEditBase(UpdateView):
    model = RegistroHoraExtra
    fields = ['motivo', 'horas']
    # QUANDO NÃO DEFINIMOS UMA def get_success_url(self): O DJANGO BUSCA O METODO PADRÃO get_absolute_url NO MODEL


class HoraExtraEdit(UpdateView):
    model = RegistroHoraExtra
    fields = ['motivo', 'horas']
    # LINHA ABAIXO VOLTA PARA A LISTAGEM APOS O SUCESSO
    # success_url = reverse_lazy('list_hora_extra')

    # ENCAMINHA PARA A TELA DE EDIÇÃO DA HORA EXTRA QUE FOI ALTERADA
    def get_success_url(self):
        # REDIRECIONA PARA TELA DE EDIÇÃO DA HORA EXTRA ALTERADA, PASSANDO O ID DA HR EXTRA COMO PARAMETRO
        # return reverse_lazy('update_hora_extra_base', args=[self.object.id])

        return reverse_lazy('update_funcionario', args=[self.object.funcionario.id])



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


class UsouHoraExtra(View):

    def post(self, *args, **kwargs):

        # ID É O PARAMETRO PK Q ESTA SENDO PASSADO POR PARAMETRO NA ROTA(URL) E VEM DENTRO DO **KWARGS
        registro_hora_extra = RegistroHoraExtra.objects.get(id=kwargs['pk'])
        registro_hora_extra.utilizada = True
        registro_hora_extra.save()

        # CRIANDO RESPOSTA JSON PARA REQUISIÇÃO AJAX
        response = json.dumps({'mensagem': 'Sucesso'})

        return HttpResponse(response, content_type='application/json')


class NaoUsouHoraExtra(View):

    def post(self, *args, **kwargs):

        # ID É O PARAMETRO PK Q ESTA SENDO PASSADO POR PARAMETRO NA ROTA(URL) E VEM DENTRO DO **KWARGS
        registro_hora_extra = RegistroHoraExtra.objects.get(id=kwargs['pk'])
        registro_hora_extra.utilizada = False
        registro_hora_extra.save()

        # CRIANDO RESPOSTA JSON PARA REQUISIÇÃO AJAX
        response = json.dumps({'mensagem': 'Sucesso'})

        return HttpResponse(response, content_type='application/json')

class ExportarExcel(View):
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="relatorio.xls" '

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Banco de horas')

        lista_colunas = ['Id', 'Motivo', 'Funcionario', 'Horas extras disponiveis', 'Horas']

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for coluna in range(len(lista_colunas)):
            ws.write(0, coluna, lista_colunas[coluna], font_style)

        # RESETANDO A FONTE PRO PADRÃO, PARA SER COLOCADO NAS LINHAS
        font_style = xlwt.XFStyle()

        lista_registros = RegistroHoraExtra.objects.filter(utilizada=False)

        linha = 1

        for registro in lista_registros:
            ws.write(linha, 0, registro.id)
            ws.write(linha, 1, registro.motivo)
            ws.write(linha, 2, registro.funcionario.nome)
            ws.write(linha, 3, registro.funcionario.total_hora_extra)
            ws.write(linha, 4, registro.horas)
            linha += 1

        wb.save(response)

        return response









