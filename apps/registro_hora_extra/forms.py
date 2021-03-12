from django.forms import ModelForm

from apps.funcionarios.models import Funcionario
from apps.registro_hora_extra.models import RegistroHoraExtra


class RegistroHoraExtraForm(ModelForm):
    def __init__(self, user, *args, **kargs):
        super(RegistroHoraExtraForm, self).__init__(*args, **kargs)

        # FILTRANDO APENAS OS FUNCIONARIOS DA EMPRESA DO USUARIO LOGADO, PARA APRESENTAR NO COMBO BOX
        empresa_funcionario = Funcionario.objects.filter(user=user)[0].empresa
        self.fields['funcionario'].queryset = Funcionario.objects.filter(empresa=empresa_funcionario)

    class Meta:
        model = RegistroHoraExtra
        fields = ['motivo', 'funcionario', 'horas']
