# TASK QUE O CELERY IRA EXECUTAR
from celery import shared_task

from django.core.mail import send_mail


@shared_task
def send_relatorio():
    send_mail(
        'ASSUNTO - TESTE RELÁTORIO CELERY',
        'MENSAGEM - TESTE',
        'gabriel.cruz.oliveira2@gmail.com',
        ['gabriel.cruz2@hotmail.com'],
    )

    return True

