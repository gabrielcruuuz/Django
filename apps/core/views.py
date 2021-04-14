from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.funcionarios.models import Funcionario

from .tasks import send_relatorio

# PROTEGENDO O CONTROLLER PARA ACESSAR APENAS ESTANDO LOGADO
@login_required
def home(request):
    data = {}

    # pegando usuario logado que fez o request
    usuario = request.user

    funcionario = Funcionario.objects.get(user=usuario)

    data['funcionario'] = funcionario
    return render(request, 'core/index.html', data)


def celery(request):
    send_relatorio.delay()
    return HttpResponse('Tarefa incluida na fila do Celery')

