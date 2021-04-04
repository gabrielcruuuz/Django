import xlwt

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views import View

from .models import Funcionario


class FuncionariosList(ListView):
    model = Funcionario
    paginate_by = 10

# SOBRESCENDO METODO DE LISTAGEM PADRÃO DO DJANGO
    def get_queryset(self):
        funcionario_logado = Funcionario.objects.get(user=self.request.user)
        empresa_funcionaro_logado = funcionario_logado.empresa
        queryset = Funcionario.objects.filter(empresa=empresa_funcionaro_logado)

        return queryset


class FuncionarioEdit(UpdateView):
    model = Funcionario
    fields = ['nome', 'lista_departamentos']


class FuncionarioDelete(DeleteView):
    model = Funcionario
    success_url = reverse_lazy('list_funcionarios')


class FuncionarioCreate(CreateView):
    model = Funcionario
    fields = ['nome', 'lista_departamentos']

    def form_valid(self, form):
        # cria o objeto mas ainda não salva no banco
        funcionario_novo = form.save(commit=False)

        if ' ' not in funcionario_novo.nome:
            username_funcionario_novo = funcionario_novo.nome
        else:
            username_funcionario_novo = funcionario_novo.nome.split(' ')[0] + funcionario_novo.nome.split(' ')[1]

        empresa_usuario_logado = Funcionario.objects.filter(user=self.request.user)[0].empresa
        funcionario_novo.empresa = empresa_usuario_logado

        # criando um usuario pra associnar ao funcionario
        funcionario_novo.user = User.objects.create(username=username_funcionario_novo)

        funcionario_novo.save()

        return super(FuncionarioCreate, self).form_valid(form)


class ExportarExcel(View):
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="relatorio_funcionarios.xls" '

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Banco de horas')

        lista_colunas = ['Id', 'Nome', 'Empresa']

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for coluna in range(len(lista_colunas)):
            ws.write(0, coluna, lista_colunas[coluna], font_style)

        # RESETANDO A FONTE PRO PADRÃO, PARA SER COLOCADO NAS LINHAS
        font_style = xlwt.XFStyle()

        empresa_usuario_logado = Funcionario.objects.filter(user=self.request.user)[0].empresa

        lista_registros = Funcionario.objects.filter(empresa=empresa_usuario_logado)

        linha = 1

        for registro in lista_registros:
            ws.write(linha, 0, registro.id)
            ws.write(linha, 1, registro.nome)
            ws.write(linha, 2, registro.empresa.nome)
            linha += 1

        wb.save(response)

        return response



