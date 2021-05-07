from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.funcionarios.models import Funcionario

from .tasks import send_relatorio

from ..registro_hora_extra.models import RegistroHoraExtra

# PROTEGENDO O CONTROLLER PARA ACESSAR APENAS ESTANDO LOGADO
@login_required
def home(request):
    data = {}

    # pegando usuario logado que fez o request
    usuario = request.user

    funcionario = Funcionario.objects.get(user=usuario)

    data['funcionario'] = funcionario
    data['total_funcionarios'] = funcionario.empresa.total_funcionarios
    data['total_funcionarios_ferias'] = funcionario.empresa.total_funcionarios_ferias
    data['total_funcionarios_doc_pendente'] = funcionario.empresa.total_funcionarios_doc_pendente

    data['total_horas_extras_utilizadas'] = RegistroHoraExtra.objects.filter(
        funcionario__empresa=funcionario.empresa, utilizada=True).aggregate(Sum('horas'))['horas__sum']

    data['total_horas_extras_pendente'] = RegistroHoraExtra.objects.filter(
        funcionario__empresa=funcionario.empresa, utilizada=False).aggregate(Sum('horas'))['horas__sum']

    return render(request, 'core/index.html', data)


def celery(request):
    # EXECUTANDO FUNÇÃO DO CELERY COM DELAY()
    send_relatorio.delay()
    return HttpResponse('Tarefa incluida na fila do Celery')

