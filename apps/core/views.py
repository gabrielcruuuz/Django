from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.funcionarios.models import Funcionario

# PROTEGENDO O CONTROLLER PARA ACESSAR APENAS ESTANDO LOGADO
@login_required
def home(request):
    data = {}

    # pegando usuario logado que fez o request
    usuario = request.user

    funcionario = Funcionario.objects.get(user=usuario)

    data['funcionario'] = funcionario
    return render(request, 'core/index.html', data)
