from rest_framework import serializers
from apps.funcionarios.models import Funcionario
from apps.registro_hora_extra.API.serializers import HoraExtraSerializer


class FuncionarioSerializer(serializers.ModelSerializer):
    # USANDO OBJETO DENTRO DE OUTRO NA RESPOSTA DA API
    registrohoraextra_set = HoraExtraSerializer(many=True)

    class Meta:
        model = Funcionario
        fields = ['id', 'nome', 'lista_departamentos', 'empresa', 'total_hora_extra', 'registrohoraextra_set']
