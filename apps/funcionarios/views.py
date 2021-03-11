from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
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


